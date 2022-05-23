Play:

```
python -i main.py
>>> e = Encoder(message="this is data", key="my_key",image="images/original.png")
>>> e.encode()
'bydRVLwjuA.png'
>>> d = Decoder(key="my_key", image="bydRVLwjuA.png")
>>> d.decode()
'this is data'
>>> d.get_data()
'this is data'
```
