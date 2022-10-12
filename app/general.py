from flask import request, render_template,redirect,url_for
from app import app

@app.errorhandler(404)
@app.errorhandler(405)
def _handle_api_error(ex):
    if "//proxy." in request.url:
        app.logger.debug("proxy")
        return redirect(url_for("proxy.page_not_found"))
    elif "//account." in request.url:
        app.logger.debug("acc")
        return redirect(url_for("account.page_not_found"))
    elif "//console." in request.url:
        app.logger.debug("dash")
        return redirect(url_for("console.page_not_found"))
    else:
        return ex


