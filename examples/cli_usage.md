# CLI Usage Examples

## Installation

First, install ublkit:
```bash
pip install ublkit
```

## Basic Commands

### Convert Single File to JSON

```bash
ublkit convert invoice.xml --format json --output output.json --config ublkit.yaml
```

### Convert Single File to CSV

```bash
ublkit convert invoice.xml --format csv --output output.csv --config ublkit.yaml
```

### Batch Convert Directory to JSON

```bash
ublkit batch ./xml_files ./output --format json --config ublkit.yaml
```

### Batch Convert Directory to CSV

```bash
ublkit batch ./xml_files ./output --format csv --config ublkit.yaml
```

### Dry Run (Preview)

Preview what would be converted without actually writing files:

```bash
ublkit batch ./xml_files ./output --format json --config ublkit.yaml --dry-run
```

## Getting Help

```bash
# Show version
ublkit --version

# Show general help
ublkit --help

# Show help for convert command
ublkit convert --help

# Show help for batch command
ublkit batch --help
```

## Configuration

Create a `ublkit.yaml` configuration file in your project directory:

```yaml
logging:
  level: "INFO"
  file: "ublkit.log"
  rotation: "500 MB"
  retention: "10 days"
  compression: "zip"

processing:
  max_workers: 4
  encoding: "utf-8"

csv:
  max_records_per_file: 50000
  preservation_method: "apostrophe"
  key_separator: " | "

output:
  summary_dir: "./summaries"
  logs_dir: "./logs"

features:
  enable_dry_run: false
```

## Complete Workflow Example

```bash
# 1. Create config file
cat > ublkit.yaml << EOF
logging:
  level: "INFO"
  file: "ublkit.log"
processing:
  max_workers: 4
  encoding: "utf-8"
csv:
  max_records_per_file: 50000
  preservation_method: "apostrophe"
  key_separator: " | "
output:
  summary_dir: "./summaries"
  logs_dir: "./logs"
features:
  enable_dry_run: false
EOF

# 2. Convert all XML files to CSV
ublkit batch ./input_xml ./output_csv --format csv --config ublkit.yaml

# 3. Check the summary
cat ./summaries/ublkit_summary_*.json

# 4. View logs
cat ./logs/ublkit.log
```

## Tips

- Always specify the config file path - it's required
- Use dry-run mode to preview changes before processing
- Check the summary file for detailed results
- Large CSV files are automatically split based on max_records_per_file
- Failed files don't stop batch processing - check summary for errors
