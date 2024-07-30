using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using System.IO;

class Program
{
    public static async Task PostFileAsync()
    {
        var url = "http://localhost:8080/";
        var filePath = "/home/x/Documents/file.txt";
        var authToken = "secure_token";

        using (var httpClient = new HttpClient())
        using (var fileStream = new FileStream(filePath, FileMode.Open, FileAccess.Read))
        using (var content = new MultipartFormDataContent())
        using (var fileContent = new StreamContent(fileStream))
        {
            // Set file content headers
            fileContent.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");
            content.Add(fileContent, "file", Path.GetFileName(filePath));

            // Set cookies
            var cookieContainer = new System.Net.CookieContainer();
            cookieContainer.Add(new Uri(url), new System.Net.Cookie("auth_token", authToken));
            var handler = new HttpClientHandler { CookieContainer = cookieContainer };

            // Send POST request
            using (var client = new HttpClient(handler))
            {
                var response = await client.PostAsync(url, content);

                // Print status code and response text
                Console.WriteLine((int)response.StatusCode);
                var responseText = await response.Content.ReadAsStringAsync();
                Console.WriteLine(responseText);
            }
        }
    }

    static void Main(string[] args)
    {
        PostFileAsync().Wait();
    }
}
