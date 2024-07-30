# Testing the execution

```
python3 make_dict_v1.py
./random_binary.sh randombinary.bin 400
python3 base64_converter.py encode randombinary.bin randombinary.base64
python3 encode_v2.py assignments.json randombinary.base64 > randombinary.encoded
python3 decode_v2.py assignments.json randombinary.encoded > randombinary.decoded
python3 base64_converter.py decode randombinary.decoded randombinary1.bin
md5sum *.bin
```

```
python3 make_dict_v3.py words.txt assignments.json
./random_binary.sh randombinary.bin 400
python3 base64_converter.py encode randombinary.bin randombinary.base64
python3 encode_v2.py assignments.json randombinary.base64 > randombinary.encoded
python3 decode_v2.py assignments.json randombinary.encoded > randombinary.decoded
python3 base64_converter.py decode randombinary.decoded randombinary1.bin
md5sum *.bin
```
