# Testing the execution

```
python3 make_dict_v1.py words.txt assignments.json
chmod +x GenerateRandomBinary_v1.sh
./GenerateRandomBinary_v1.sh randombinary.bin 400
python3 base64converter_v1.py encode randombinary.bin randombinary.base64
python3 encode_v1.py assignments.json randombinary.base64 > randombinary.encoded
python3 decode_v1.py assignments.json randombinary.encoded > randombinary.decoded
python3 base64converter_v1.py decode randombinary.decoded randombinary1.bin
md5sum *.bin
```
