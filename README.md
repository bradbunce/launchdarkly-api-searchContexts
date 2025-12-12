# LaunchDarkly Context Search Tool

A Python script to search and analyze contexts in LaunchDarkly using the LaunchDarkly API.

## Features

- Search for contexts based on configurable filters
- Export context data to CSV
- Evaluate feature flag values for each context
- Handle pagination automatically for large result sets
- Progress tracking and detailed logging

## Prerequisites

- Python 3.6+
- Valid LaunchDarkly API key
- Access to a LaunchDarkly project and environment

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd launchdarkly-api-searchContexts
   ```

2. Install required dependencies:
   ```bash
   pip3 install python-dotenv
   ```

3. Set up your environment variables by copying the example file:
   ```bash
   cp .env.example .env
   ```

4. Edit the `.env` file with your actual LaunchDarkly configuration:
   ```bash
   nano .env
   ```

## Configuration

Update the `.env` file with your LaunchDarkly settings:

```env
apiKey=your-launchdarkly-api-key
projectKey=your-project-key
environmentKey=your-environment-key
connectionUrl=app.launchdarkly.com
contextFilter=user.appVersion equals 6.23.1,user.region equals NA,user.appBrand equals Buick
sort=-ts
limit=50
featureFlagKey=your-feature-flag-key
outputFile=/path/to/your/output.csv
```

### Configuration Parameters

- **apiKey**: Your LaunchDarkly API key (get from Account Settings > Authorization)
- **projectKey**: The key of your LaunchDarkly project
- **environmentKey**: The environment key (e.g., production, staging)
- **connectionUrl**: LaunchDarkly API URL (typically `app.launchdarkly.com`)
- **contextFilter**: Comma-separated list of context filters
- **sort**: Sort order (`ts` for ascending, `-ts` for descending by timestamp)
- **limit**: Maximum number of items per API call (max: 50, default: 20)
- **featureFlagKey**: Feature flag key for evaluation
- **outputFile**: Path where CSV output will be saved

## Usage

Run the script:

```bash
python3 searchContexts.py
```

The script will:
1. Search for contexts matching your filter criteria
2. Display progress information including total count and percentage retrieved
3. Evaluate feature flag values for each unique context
4. Output results to the console

## Output

The script provides detailed console output including:
- Total context count found
- Number of contexts retrieved in each batch
- Percentage of total contexts processed
- Feature flag evaluations for each context

## CSV Export

To enable CSV export, uncomment the line in the `main()` function:

```python
def main():
    response = get_contexts()
    export_contexts_to_csv(response)  # Uncomment this line
    contextKeys = export_contexts(response)
    get_feature_flag_variations_for_contexts(contextKeys)
```

## Error Handling

The script includes error handling for:
- Invalid API keys (401 Unauthorized)
- Network connectivity issues
- Empty result sets
- API rate limiting (includes 2-second delays between flag evaluations)

## Security

- The `.env` file is included in `.gitignore` to prevent accidental commit of sensitive data
- Never commit your actual API keys to version control
- Use the `.env.example` file as a template for others

## Troubleshooting

### 401 Unauthorized Error
- Verify your API key is valid and not expired
- Check that your API key has the necessary permissions
- Ensure the project and environment keys are correct

### No Results Returned
- Verify your context filter syntax
- Check that contexts matching your criteria exist
- Ensure your API key has read access to the specified project/environment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.