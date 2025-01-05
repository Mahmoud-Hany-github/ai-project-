from qlib.config import REG_CN
from qlib.workflow import R
import qlib

# Initialize Qlib
qlib.init(provider_uri="data/processed/qlib_data", region=REG_CN)  # Update path if needed
print("Qlib initialized!")
