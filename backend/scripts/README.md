# 🚀 Dosa Club Backend Scripts

This directory contains enhanced utility scripts for managing the DosaClub backend, including database setup, data seeding, and maintenance. All scripts feature beautiful console output, skip logic, and comprehensive error handling.

## 📋 Prerequisites

### 1. Environment Variables
Ensure you have a `.env` file in the `backend/` directory (one level up).

**Example `.env`:**
```env
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
DYNAMODB_ENDPOINT=http://localhost:8000  # Or use AWS real endpoint

# Application Settings
DEBUG=true
LOG_LEVEL=DEBUG
```

### 2. Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. DynamoDB Setup
- **Local Development**: Run DynamoDB Local on port 8000
- **Production**: Use AWS DynamoDB with proper IAM roles

## 🎯 Quick Start Guide

### Option 1: Run All Scripts (Recommended)
```bash
cd scripts
python run_all.py
```

### Option 2: Manual Setup
Run these scripts in order for a fresh environment:

```bash
# 1. Create database tables
python setup_core_tables.py

# 2. Seed menu items
python seed_menu_items.py

# 3. Seed health rules
python seed_health_rules.py

# 4. Create test users
python seed_test_users.py

# 5. Setup guest sessions
python setup_guest_sessions.py
```

## 🛠️ Enhanced Scripts Overview

| Script | Description | Safe to Re-run? |
|--------|-------------|-----------------|
| `run_all.py` | 🚀 **Master Runner** - Executes all scripts in order | ✅ Yes |
| `setup_core_tables.py` | 🗄️ Creates 6 core DynamoDB tables | ✅ Yes |
| `seed_menu_items.py` | 🍽️ Seeds 45+ South Indian food items | ✅ Yes |
| `seed_menu_images.py` | 🖼️ Assigns images to menu items without them | ✅ Yes |
| `seed_health_rules.py` | 🏥 Creates health recommendation rules | ✅ Yes |
| `seed_test_users.py` | 👤 Creates test user profiles | ✅ Yes |
| `setup_guest_sessions.py` | 🎫 Sets up guest session management | ✅ Yes |
| `cleanup_sessions.py` | 🧹 Cleans expired guest sessions | ✅ Yes |

## 📊 Database Schema

### Core Tables Created:
1. **users** - User profiles and health data
2. **menu_items** - Food catalog with nutritional info
3. **health_rules** - BMI/condition → item mappings
4. **suggestions_log** - Recommendation history
5. **favorites** - User favorite items
6. **guest_sessions** - Temporary anonymous sessions

## 🎨 Script Features

### Enhanced Console Output
```
🍽️  DOSA CLUB - MENU ITEMS SEEDER
⏰ Started at: 2026-02-02 16:45:30
📍 DynamoDB Endpoint: AWS (Real Service)
📦 Processing 45 menu items...
✅ [  1/45] ADDED: Plain Dosa (ID: a1b2c3d4...)
⏭️  [  2/45] SKIPPING: Masala Dosa (already exists)
📊 SUMMARY:
   ✅ Added: 12 new items
   ⏭️  Skipped: 33 existing items
   ❌ Errors: 0 items
🎉 Menu items seeding completed successfully!
```

### Skip Logic & Safety
- ✅ **Idempotent** - Safe to run multiple times
- ✅ **Duplicate Detection** - Checks existing data before insertion
- ✅ **Graceful Errors** - Continues processing on individual failures
- ✅ **Progress Tracking** - Real-time status updates

### Error Handling
- 🛡️ **AWS Credential Validation** - Clear error messages for missing credentials
- 🛡️ **Table Existence Checks** - Verifies tables exist before operations
- 🛡️ **Network Error Recovery** - Handles connection issues gracefully
- 🛡️ **Data Validation** - Validates data structure before insertion

## � Detailed Script Usage

### 1. Master Runner (`run_all.py`)
**Purpose**: Execute all setup scripts in correct order
```bash
python run_all.py
```
**Features**:
- Runs scripts in dependency order
- Captures and displays output
- Stops on critical failures
- Provides overall status summary

### 2. Core Tables Setup (`setup_core_tables.py`)
**Purpose**: Creates all necessary DynamoDB tables
```bash
python setup_core_tables.py
```
**Tables Created**:
- `users` (user_id: String)
- `menu_items` (item_id: String)
- `health_rules` (rule_id: String)
- `suggestions_log` (suggestion_id: String)
- `favorites` (favorite_id: String)
- `guest_sessions` (session_id: String)

### 3. Menu Items Seeder (`seed_menu_items.py`)
**Purpose**: Populates menu catalog with South Indian dishes
```bash
python seed_menu_items.py
```
**Data Source**: `seed_data.py` (45+ items)
**Categories**: Dosa, Idli, Vada, Uthappam, Beverages
**Features**: Nutritional info, spice levels, dietary tags

### 4. Menu Images Seeder (`seed_menu_images.py`)
**Purpose**: Updates existing menu items with random consistent images from uploads
```bash
python seed_menu_images.py
```
**Features**:
- Deterministic image assignment based on item name
- Skips items that already have images
- Uses local assets directory

### 5. Health Rules Seeder (`seed_health_rules.py`)
**Purpose**: Creates intelligent recommendation rules
```bash
python seed_health_rules.py
```
**Rules Include**:
- BMI categories (underweight, normal, overweight, obese)
- Medical conditions (diabetes, bp, acidity)
- Dietary preferences (veg, egg)
- Spice tolerance levels

### 6. Test Users (`seed_test_users.py`)
**Purpose**: Creates sample user profiles for testing
```bash
python seed_test_users.py
```
**Sample Users**:
- Various BMI categories
- Different medical conditions
- Multiple dietary preferences

### 7. Guest Sessions (`setup_guest_sessions.py`)
**Purpose**: Sets up temporary session management
```bash
python setup_guest_sessions.py
```
**Features**:
- 30-minute session expiry
- Anonymous user support
- Automatic cleanup capability

### 8. Cleanup Script (`cleanup_sessions.py`)
**Purpose**: Removes expired guest sessions
```bash
python cleanup_sessions.py
```
**Automation**: Can be run as cron job
```bash
# Add to crontab for hourly cleanup
0 * * * * cd /path/to/backend/scripts && python cleanup_sessions.py
```

## 🔧 Configuration

### Environment Variables
```env
# Required
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here
AWS_REGION=us-east-1

# Optional
DYNAMODB_ENDPOINT=http://localhost:8000  # Local DynamoDB
DEBUG=true
LOG_LEVEL=DEBUG
```

### Script Customization
- **Batch Sizes**: Modify processing batch sizes in individual scripts
- **Timeout Settings**: Adjust AWS operation timeouts
- **Retry Logic**: Configure retry attempts for failed operations
- **Logging Levels**: Set DEBUG, INFO, WARNING, ERROR

## ❓ Troubleshooting

### Common Issues & Solutions

#### ❌ "AWS credentials not found"
**Cause**: Missing or incorrect `.env` file
**Solution**:
```bash
# Check .env exists
ls -la ../.env

# Verify format
cat ../.env
```

#### ❌ "EndpointConnectionError"
**Cause**: DynamoDB not accessible
**Solution**:
```bash
# For local DynamoDB
curl http://localhost:8000

# For AWS, check network connectivity
ping dynamodb.us-east-1.amazonaws.com
```

#### ❌ "Table already exists"
**Cause**: Normal behavior, scripts handle this gracefully
**Solution**: No action needed - scripts skip existing tables

#### ❌ "Permission denied"
**Cause**: Insufficient AWS permissions
**Solution**:
- Check IAM policies
- Verify DynamoDB access permissions
- Ensure proper region configuration

### Debug Mode
Enable detailed logging:
```bash
export LOG_LEVEL=DEBUG
python setup_core_tables.py
```

### Dry Run Mode
Some scripts support dry-run mode to preview changes:
```bash
python seed_menu_items.py --dry-run
```

## 🔄 Maintenance

### Regular Tasks
1. **Session Cleanup**: Run `cleanup_sessions.py` hourly/daily
2. **Data Updates**: Use seeders to update menu items/rules
3. **Backup**: Export critical data before major updates
4. **Monitoring**: Check script execution logs

### Production Deployment
```bash
# Set production environment
export ENVIRONMENT=production
export LOG_LEVEL=INFO

# Run setup
python run_all.py

# Verify setup
python -c "
import asyncio
from app.services.dynamodb import DynamoDBClient
async def check():
    db = DynamoDBClient()
    print('Tables ready!')
asyncio.run(check())
"
```

## 📚 Additional Resources

- **DynamoDB Documentation**: https://docs.aws.amazon.com/dynamodb/
- **FastAPI Best Practices**: https://fastapi.tiangolo.com/
- **Python Async Programming**: https://docs.python.org/3/library/asyncio.html

---

## 🎉 Success Indicators

When scripts run successfully, you should see:
- ✅ All tables created (first run) or skipped (subsequent runs)
- ✅ Menu items seeded (45+ items)
- ✅ Health rules configured (16+ rules)
- ✅ Test users created
- ✅ Guest sessions ready
- 🎉 "All scripts completed successfully!" message

Your Dosa Club backend is now ready for development or production! 🚀
