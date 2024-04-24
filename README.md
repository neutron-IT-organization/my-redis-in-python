# Redis-like Server in Python

A simplified implementation of a Redis-like server using Python.

## Overview

This project provides a basic implementation of a Redis-like server using Python. The server listens for client connections, interprets commands using the Redis Serialization Protocol (RESP), and performs corresponding actions.

## Features

- **Server Setup:** Listens for client connections on port `6379` using Python's `socket` module.
- **Protocol Handling:** Implements the Redis Serialization Protocol (RESP) for communication.
- **Command Interpretation:** Reads and interprets Redis-like commands to execute appropriate actions.
- **Extendable:** Designed for extending with additional commands and features.

## Getting Started

### Prerequisites

- Python 3.x
- `redis-cli` for testing

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/neutron-IT-organization/my-redis-in-python.git
    ```

2. Navigate to the project directory:

    ```bash
    cd redis-like-python
    ```

### Running the Server

Run the `main.py` script to start the server:

```bash
python main.py
```

The server will start listening for connections on port `6379`.

### Testing with `redis-cli`

You can test the server using `redis-cli`, the command-line Redis client.

1. Open a new terminal window.

2. Connect to the server:

    ```bash
    redis-cli -h localhost -p 6379
    ```

3. Now you can send Redis commands:

    ```bash
    SET mykey "Hello"
    ```

4. To retrieve the value:

    ```bash
    GET mykey
    ```

You should see the value `"Hello"` returned by the server.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

