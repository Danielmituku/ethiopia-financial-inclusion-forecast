# Ethiopia Financial Inclusion Unified Dataset

## Overview

This dataset uses a **unified schema** where all records share the same structure. The `record_type` field indicates how to interpret each row.

## Record Types

| record_type | Count | Description |
|-------------|-------|--------------|
| observation | 30+ | Measured values (Findex surveys, operator reports, infrastructure data) |
| event | 10 | Policies, product launches, market entries, milestones |
| impact_link | 14 | Modeled relationships between events and indicators |
| target | 3 | Official policy goals (e.g., NFIS-II targets) |

## Key Indicator Codes

### Access Indicators
- `ACC_OWNERSHIP` - Account ownership rate (% adults)
- `ACC_MM_ACCOUNT` - Mobile money account ownership (% adults)
- `ACC_OWNERSHIP_M` - Account ownership male (% adult males)
- `ACC_OWNERSHIP_F` - Account ownership female (% adult females)
- `ACC_TELEBIRR_USERS` - Telebirr registered users (count)
- `ACC_MPESA_USERS` - M-Pesa registered users (count)

### Usage Indicators
- `USG_DIGITAL_PAYMENT` - Made/received digital payment (% adults)
- `USG_WAGE_ACCOUNT` - Received wages into account (% adults)

### Infrastructure Indicators
- `INF_4G_COVERAGE` - 4G population coverage (%)
- `INF_MOBILE_PEN` - Mobile phone penetration (% population)

## Data Sources

1. **Global Findex Database** - World Bank triennial surveys (2011, 2014, 2017, 2021, 2024)
2. **Ethio Telecom** - Telebirr operational data
3. **Safaricom Ethiopia** - M-Pesa operational data
4. **ITU** - Infrastructure and connectivity data
5. **National Bank of Ethiopia** - Policy documents and regulatory data
6. **EthSwitch** - Payment system interoperability data
