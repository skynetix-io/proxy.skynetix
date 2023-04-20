import logging
from app import app
# from app.models import Gestori,Soci,Corsi,CorsiPerSocio,Ricevute,MensilePagati,Extra,ExtraPagati,Incassi,InsegnatiPerCorso,EventiPerSocio,Insegnanti,Stipendi,Uscite
# import os 
# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'Gestori': Gestori, 'Corsi':Corsi,'CorsiPerSocio':CorsiPerSocio,'Ricevute':Ricevute,"Insegnanti":Insegnanti,'Soci':Soci,'MensilePagati':MensilePagati,'Extra':Extra,'ExtraPagati':ExtraPagati,"Incassi":Incassi,"IPC":InsegnatiPerCorso,"EventiPerSocio":EventiPerSocio,"Stipendi":Stipendi,"Uscite":Uscite}


if __name__ == "__main__":
    app.run(host='skynetix.io', port=5000, debug=True)

else:
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
