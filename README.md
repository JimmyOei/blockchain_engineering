# Blockchain Engineering Assignments

## General Setup

Use Python 3.10+ and a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Each lab folder now has its own `requirements.txt`.

## Instructions Lab 1

### Setup

Install dependencies for Lab 1:

```bash
cd lab1
pip install -r requirements.txt
```


### Usage

```bash
python lab1.py
```

When running the algorithm the first time a private key is generated and stored in `lab1/labs-ec.pem`. It is important to store this private key safely.

## Instructions Lab 2
Copy the private key generated when running Lab 1 (`lab1/labs-ec.pem`) into the `lab2` folder as `lab2/my_key.pem`.
Also store each member's public key (hex-encoded) in:

- `lab2/first_key.txt`
- `lab2/second_key.txt`
- `lab2/third_key.txt`

### Setup

```bash
cd lab2
pip install -r requirements.txt
```

Set your member index before running (`0`, `1`, or `2`):

```bash
export MY_MEMBER_ID=0
```


### Usage

```bash
python main.py
```

## Instructions Lab 3
Copy the private key generated in Lab 1 (`lab1/labs-ec.pem`) into the `lab3` folder as `lab3/my_key.pem`.
Also store each member's public key (hex-encoded) in:

- `lab3/first_key.txt`
- `lab3/second_key.txt`
- `lab3/third_key.txt`


### Setup

```bash
cd lab3
pip install -r requirements.txt
```

Set your member index before running (`0`, `1`, or `2`):

```bash
export MY_MEMBER_ID=0
```


### Usage

```bash
python main.py
```

#### For the forking bonus assignment:

For the forking bonus assignment, we implemented a forking mechanism that allows peers to maintain the strongest chain even after a partition occured. We also implemented a polling mechanism that allows peers to check if another peer has a stronger chain that it can switch to.

If you want to create a partition, set `PARTITION_TEST_ENABLED` to True in `lab3/constants.py` for the peer that you want separated. After 30 seconds of running the peer will start to ignore messages and will not send messages to other peers. After another 30 seconds it will try to reconnect again.