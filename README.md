Play:

```
python -i main.py
>>> e = Encoder("this is data", "images/original.png")
>>> e.encode()
'bydRVLwjuA.png'
>>> d = Decoder("bydRVLwjuA.png")
>>> d.decode()
'this is data'
>>> d.get_data()
'this is data'
```
