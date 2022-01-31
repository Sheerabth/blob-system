from src.main import app
import uvicorn
import logging.handlers

if __name__ == "__main__":
    handler = logging.handlers.RotatingFileHandler("server.log", maxBytes=4194304)
    logging.basicConfig(
        handlers=[handler], format="%(levelname)s: %(filename)s[%(lineno)s] - %(message)s", level=logging.INFO
    )
    uvicorn.run(app, host="0.0.0.0", port=8080, log_config=None)
