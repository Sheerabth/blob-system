from src.main import app
import uvicorn
import logging

if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(filename)s[%(lineno)s] - %(message)s", level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8080, log_config=None)
