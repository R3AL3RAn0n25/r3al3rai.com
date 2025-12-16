# Environment Setup

This project requires several environment variables to be set for proper operation. These should be set in a `.env` file in the root directory of the project.

## Required Environment Variables

- `SECRET_KEY`: Used for session security (generate a strong random key)
- `ADMIN_PASSWORD`: Administrator password (use a strong password)
- `MONGO_URI`: MongoDB connection string (without credentials in the repository)

## Optional Environment Variables

- `ADAPTATION_COOLDOWN`: Cooldown period in seconds (default: 60)
- `MAX_INSIGHTS_BEFORE_REVIEW`: Maximum insights before review (default: 100)
- `JWT_EXPIRY_SECONDS`: JWT token expiry in seconds (default: 86400)

## Setting Up Environment Variables

1. Create a `.env` file in the root directory
2. Add the required environment variables with your values
3. Never commit the `.env` file to version control

Example `.env` file:
```
SECRET_KEY=your_generated_secret_key
ADMIN_PASSWORD=your_strong_password
MONGO_URI=mongodb+srv://${MONGO_USER}:${MONGO_PASSWORD}@${MONGO_HOST}
```

## Security Notes

- Never commit credentials to version control
- Use strong, randomly generated values for secrets
- Rotate credentials regularly
- Use different credentials for development and production