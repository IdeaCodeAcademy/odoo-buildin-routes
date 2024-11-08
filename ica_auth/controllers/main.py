from odoo import http
from odoo.http import request


class MainController(http.Controller):
    @http.route('/api/login', type='json', auth="none")
    def api_login(self, **kw):
        credentials = {'login': kw.get('login'), 'password': kw.get('password'),'type':'password'}
        data = request.session.authenticate(request.session.db, credentials)
        return {"message": "Login Successful.", "data": data}
