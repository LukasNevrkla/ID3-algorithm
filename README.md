# ID3 algorithm

## Usage

```
python3 ID3.py <json-data>
```

## Example JSON data

```
{
   "attributes":{
      "oblacnost":[
         "polojasno",
         "oblacno",
         "zatazeno"
      ],
      "srazky":[
         "slabe",
         "vydatne"
      ],
      "teplota":[
         "nizka",
         "stredni",
         "vysoka"
      ],
      "vhkost":[
         "mala",
         "velka"
      ]
   },
   "classes":[
      "Q",
      "R",
      "S"
   ],
   "objects":[
      [
         "1",
         "R",
         "oblacno",
         "slabe",
         "vysoka",
         "mala"
      ],
      [
         "2",
         "Q",
         "oblacno",
         "vydatne",
         "stredni",
         "mala"
      ],
      [
         "3",
         "Q",
         "polojasno",
         "vydatne",
         "nizka",
         "velka"
      ],
      [
         "4",
         "S",
         "polojasno",
         "vydatne",
         "vysoka",
         "velka"
      ],
      [
         "5",
         "S",
         "oblacno",
         "vydatne",
         "nizka",
         "velka"
      ],
      [
         "6",
         "S",
         "zatazeno",
         "vydatne",
         "stredni",
         "velka"
      ],
      [
         "7",
         "R",
         "oblacno",
         "vydatne",
         "vysoka",
         "velka"
      ],
      [
         "8",
         "Q",
         "oblacno",
         "slabe",
         "stredni",
         "mala"
      ],
      [
         "9",
         "Q",
         "polojasno",
         "slabe",
         "stredni",
         "mala"
      ],
      [
         "10",
         "R",
         "polojasno",
         "slabe",
         "stredni",
         "velka"
      ],
      [
         "11",
         "Q",
         "zatazeno",
         "vydatne",
         "stredni",
         "mala"
      ],
      [
         "12",
         "Q",
         "zatazeno",
         "slabe",
         "stredni",
         "mala"
      ]
   ]
}
```

## Example output

```
Train set = examples[3:12]
-------------------------
| [vhkost] 
|    |oblacnost  = 0.168|
|    |srazky     = 0.408|
|    |teplota    = 0.474|
|    |vhkost     = 0.991|
| => mala ['8', '9', '11', '12']
|    | {'Q'}
| => velka ['4', '5', '6', '7', '10']
|    | [srazky]
|    |    |oblacnost  = 0.171|
|    |    |srazky     = 0.322|
|    |    |teplota    = 0.171|
|    | => slabe ['10']
|    |    | {'R'}
|    | => vydatne ['4', '5', '6', '7']
|    |    | [oblacnost]
|    |    |    |oblacnost  = 0.311|
|    |    |    |teplota    = 0.311|
|    |    | => polojasno ['4']
|    |    |    | {'S'}
|    |    | => oblacno ['5', '7']
|    |    |    | [teplota]
|    |    |    |    |teplota    = 1.000|
|    |    |    | => nizka ['5']
|    |    |    |    | {'S'}
|    |    |    | => stredni []
|    |    |    |    | set()
|    |    |    | => vysoka ['7']
|    |    |    |    | {'R'}
|    |    | => zatazeno ['6']
|    |    |    | {'S'}

Train set = examples[0:9]
-------------------------
| [teplota]
|    |oblacnost  = 0.379|
|    |srazky     = 0.252|
|    |teplota    = 0.642|
|    |vhkost     = 0.408|
| => nizka ['3', '5']
|    | [oblacnost]
|    |    |oblacnost  = 1.000|
|    |    |srazky     = 0.000|
|    |    |vhkost     = 0.000|
|    | => polojasno ['3']
|    |    | {'Q'}
|    | => oblacno ['5']
|    |    | {'S'}
|    | => zatazeno []
|    |    | set()
| => stredni ['2', '6', '8', '9']
|    | [oblacnost]
|    |    |oblacnost  = 0.811|
|    |    |srazky     = 0.311|
|    |    |vhkost     = 0.811|
|    | => polojasno ['9']
|    |    | {'Q'}
|    | => oblacno ['2', '8']
|    |    | {'Q'}
|    | => zatazeno ['6']
|    |    | {'S'}
| => vysoka ['1', '4', '7']
|    | [oblacnost]
|    |    |oblacnost  = 0.918|
|    |    |srazky     = 0.252|
|    |    |vhkost     = 0.252|
|    | => polojasno ['4']
|    |    | {'S'}
|    | => oblacno ['1', '7']
|    |    | {'R'}
|    | => zatazeno []
|    |    | set()
```