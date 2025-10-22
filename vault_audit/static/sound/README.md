# Sound Effects

This folder contains audio files for the Vault Audit System.

## Files

- `succesful_scan.mp3` - Success sound that plays when a scanned label matches an expected label
- `invalid_scan.m4a` - Error sound that plays when a scanned label does NOT match any expected label

## Usage

Place both sound files in this directory:
```
vault_audit/static/sound/succesful_scan.mp3
vault_audit/static/sound/invalid_scan.m4a
```

The application will automatically play the appropriate sound based on scan results:
- **Valid Scan**: Plays success sound when label is found in expected labels list
- **Invalid Scan**: Plays error sound when label is NOT found in expected labels list

## Audio Settings

### Success Sound (succesful_scan.mp3)
- **Format**: MP3
- **Trigger**: Plays when label validation returns "✓ Found"
- **Behavior**: Resets to start for each successful scan
- **Error Handling**: Fails gracefully if audio cannot play (e.g., browser autoplay restrictions)

### Invalid Sound (invalid_scan.m4a)
- **Format**: M4A (AAC)
- **Trigger**: Plays when label validation returns "✗ Not Found"
- **Behavior**: Resets to start for each invalid scan
- **Error Handling**: Fails gracefully if audio cannot play (e.g., browser autoplay restrictions)
