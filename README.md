# wp_config_replacer.py

Generate random strings needed for your wp-config.php file.

## Usage
This will set the `AUTH_KEY`, `SECURE_AUTH_KEY`, `LOGGED_IN_KEY`, `NONCE_KEY`, 
`AUTH_SALT`, `SECURE_AUTH_SALT`, `LOGGED_IN_SALT`, `NONCE_SALT` values in your 
PHP file to secure, random strings.

```sh
wp_config_replacer.py path/to/wp-config-sample.php > path/to/wp-config.php
```

These strings use the same characters and length (64) as you would get if you 
called [Wordpress's API](https://api.wordpress.org/secret-key/1.1/salt/).

## Requires
Developed for Python 3, but probably works on Python 2 as well.

Does not require any external libraries.
