import hashlib
import base64
from typing import Optional


class StringShortener:
    short_to_long = {}

    @staticmethod
    def generate_short_url(input_str: str, attempt: int = 0) -> str:
        # Combine the input string with the attempt number
        combined = f"{input_str}_{attempt}"

        # Create SHA256 hash (using a longer hash to reduce collision probability)
        sha_hash = hashlib.sha256(combined.encode()).digest()

        # Encode to Base64 and remove non-alphanumeric characters
        base64_encoded = base64.urlsafe_b64encode(sha_hash).decode('ascii')
        alphanumeric = ''.join(c for c in base64_encoded if c.isalnum())

        # Return the first 8 characters. We'll trim this later if needed.
        return alphanumeric[:8]

    @staticmethod
    def shorten_string(input_str: str) -> str:
        if not input_str:
            return input_str

        attempt = 0
        while True:
            shortened = StringShortener.generate_short_url(input_str, attempt)

            # Try lengths from 5 to 8
            for length in range(5, 9):
                current_short = shortened[:length]
                if current_short not in StringShortener.short_to_long:
                    StringShortener.short_to_long[current_short] = input_str
                    return current_short
                elif StringShortener.short_to_long[current_short] == input_str:
                    return current_short

            # If we're here, we've had a collision. Increment attempt and try again.
            attempt += 1

    @staticmethod
    def get_original_url(shortened: str) -> Optional[str]:
        return StringShortener.short_to_long.get(shortened)

    @staticmethod
    def get_shortened_url(original: str) -> Optional[str]:
        attempt = 0
        while True:
            shortened = StringShortener.generate_short_url(original, attempt)
            for length in range(5, 9):
                current_short = shortened[:length]
                if current_short in StringShortener.short_to_long and StringShortener.short_to_long[
                    current_short] == original:
                    return current_short
            attempt += 1
            if attempt > 1000:  # Prevent infinite loop, adjust as needed
                return None


# Example usage
if __name__ == "__main__":
    urls = [
        "https://www.example.com/very/long/url/that/needs/shortening",
        "https://www.anotherexample.com/another/long/url",
        "https://www.thirdexample.com/yet/another/url",
        "https://www.fourthexample.com/one/more/url",
        "https://www.fifthexample.com/last/url"
    ]

    for i, url in enumerate(urls, 1):
        shortened = StringShortener.shorten_string(url)
        print(f"Original {i}: {url}")
        print(f"Shortened {i}: {shortened} (length: {len(shortened)})")
        print(f"Retrieved: {StringShortener.get_original_url(shortened)}")
        print(f"Lookup shortened: {StringShortener.get_shortened_url(url)}")
        print()

    # Test duplicates
    duplicate = StringShortener.shorten_string(urls[0])
    print(f"Duplicate test: {duplicate} (should be same as Shortened 1)")
    print(f"Retrieved for duplicate: {StringShortener.get_original_url(duplicate)}")
    print()

    # Test many URLs to force collisions
    for i in range(1000):
        url = f"https://www.example{i}.com/{'x' * i}"
        shortened = StringShortener.shorten_string(url)
        assert StringShortener.get_original_url(shortened) == url
        assert StringShortener.get_shortened_url(url) == shortened

    print("1000 URLs processed successfully, including potential collisions.")

    # Count the distribution of shortened URL lengths
    lengths = [len(shortened) for shortened in StringShortener.short_to_long.keys()]