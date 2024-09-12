# Short URL Service

A lightweight and efficient URL shortening service built with Python. This service generates short codes for long URLs using a custom hashing algorithm.

## Features

- Generate short codes for long URLs
- Retrieve original URLs from short codes
- Collision-resistant hashing algorithm
- Configurable short code length (5-8 characters)
- In-memory storage of URL mappings
- Pure Python implementation with no external dependencies

## Prerequisites

- Python 3.6+

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/short-url-service.git
   cd short-url-service
   ```

2. No additional installation steps are required as the service uses only Python standard library modules.

## Usage

The `StringShortener` class provides the core functionality of the URL shortening service. Here's how to use it:

```python
from main import StringShortener

# Shorten a URL
long_url = "https://www.example.com/very/long/url/that/needs/shortening"
short_code = StringShortener.shorten_string(long_url)
print(f"Shortened URL: {short_code}")

# Retrieve the original URL
original_url = StringShortener.get_original_url(short_code)
print(f"Original URL: {original_url}")

# Look up the short code for an existing URL
existing_short_code = StringShortener.get_shortened_url(long_url)
print(f"Existing short code: {existing_short_code}")
```

## How It Works

1. The service uses SHA256 hashing combined with Base64 encoding to generate short codes.
2. It starts with a 5-character code and increases the length up to 8 characters to handle collisions.
3. If collisions persist, it modifies the input to the hash function and tries again.
4. The service maintains an in-memory dictionary to store mappings between short codes and original URLs.

## Limitations

- The current implementation stores URL mappings in memory, which means they are lost when the program exits.
- There's no web interface or API; it's designed to be used as a Python module.

## Future Improvements

- Implement persistent storage (e.g., database) for URL mappings.
- Create a web interface and API for easier access.
- Add user authentication and custom short code creation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
