# odoo Buildin Routes

odoo မှာ external platform တွေနဲ့ integration လုပ်လိုတဲ့အခါမှာ ကိုယ်တိုင် custom route တွေကိုရေးခြင်းကို လျှော့ချပြီး 
အသုံးပြုနိုင်တဲ့ odoo ရဲ့ buildin routes တွေအကြောင်း sharing လုပ်ပေးလိုပါတယ်။ 

api ဆိုတော့ ပုံမှန် crud တွေ ဖြစ်တဲ့ list, details, create,update,unlink စသဖြင့် ပါ၀င်ရမှာ ဖြစ်ပါတယ်။

ဒီ article အတွက် odoo version 18.0 ကို အသုံးပြုထားပြီး api knowledge အခြေခံရှိရမှာဖြစ်ပါတယ်။

postman, httpclient, thunder client တို့လို api client အတွက် tools တွေကို အသုံးပြုပြီး စမ်းသပ်နိုင်ပါတယ်။

လိုအပ်လျှင် postman collection ကို [Odoo Build In Routes.postman_collection.json](Odoo%20Build%20In%20Routes.postman_collection.json) ဒီနေတွင် ရယူနိုင်ပါသည်။

### login routes
```python
from odoo import http
from odoo.http import request


class MainController(http.Controller):
    @http.route('/api/login', type='json', auth="none")
    def api_login(self, **kw):
        credentials = {'login': kw.get('login'), 'password': kw.get('password'),'type':'password'}
        data = request.session.authenticate(request.session.db, credentials)
        return {"message": "Login Successful.", "data": data}
```

odoo က auth အတွက် cookies ကို အသုံးပြုထားတဲ့အတွက် အထက်ပါအတိုင်း login အတွက်  custom route တစ်ခုကို ရေးသားလိုက်ပါမယ်။
ထို request လုပ်ကြည့်သည့်အခါ response ထဲတွင် cookies ဆိုသည့် hader တစ်ခုပါ၀င်လာသည်ကို မြင်ရပါမည်။ 
ထို header ကို အသုံးပြုပြီး buildin route တွေကို စတင် request လုပ်ကြည့်ပါမည်။

အောက်ပါ routes များအားလုံးတွင် standard json အနေဖြင့် အောက်ပါ format တစ်ခု ရှိနေပါမည်။ request ပြုလုပ်ရမည့် route ကတော့ `{{host}}/web/dataset/call_kw` ဖြစ်ပါတယ်။

```json
//{{host}}/web/dataset/call_kw
{
  "jsonrpc": "2.0",
  "params": {
    "model": "",
    "method": "",
    "args": [],
    "kwargs": {}
  }
}
```

### web_save ( create, write )

api ကနေ create, write ပြုလုပ်လိုသည့်အခါတွင် web_save ဆိုသည့် method ကို အသုံးပြုပါသည်။ 
create အတွက်  `"args": [[],{"name": "Sample 100"}],` ဟု အသုံးပြုရမည် ဖြစ်ပြီး 
write အတွက် `"args": [[62], {"name": "Sample 100"}],` ဟု အသုံးပြုရပါမည်။ နမူနာကို အောက်တွင် ကြည့်နိုင်ပါသည်။
reponse အတွက် kwargs->specification ထဲတွင် မိမိတို့လိုအပ်သည့် fields ကို အတိအကျ request လုပ်နိုင်ပါမည်။

- create

```json 
// {{host}}/web/dataset/call_kw
{
    "jsonrpc": "2.0",
    "params": {
        "model": "res.partner",
        "method": "web_save",
        // create
         "args": [[],{"name": "Sample 100"}],
        "kwargs": {
            "specification": {
                "active": {},
                "category_id": {
                    "fields": {
                        "color": {},
                        "display_name": {}
                    }
                },
                "write_date": {}
            }
        }
    }
}
```

- write

```json 
// {{host}}/web/dataset/call_kw
{
    "jsonrpc": "2.0",
    "params": {
        "model": "res.partner",
        "method": "web_save",
//          write
         "args": [[62], {"name": "Sample 100"}],
        "kwargs": {
            "specification": {
                "active": {},
                "category_id": {
                    "fields": {
                        "color": {},
                        "display_name": {}
                    }
                },
                "write_date": {}
            }
        }
    }
}
```


### web_read (details)

web_read ကတော့ details ကို တောင်းယူလိုသည့်အခါတွင် အသုံးပြုနိုင်ပါသည်။ မိမိတို့တောင်းယူလိုသော id ကို `"args": [[46]],` ဟု ထည့်သွင်းပေးလိုက်ယုံပဲ ဖြစ်ပါတယ်။

```json 
// {{host}}/web/dataset/call_kw

{
    "jsonrpc": "2.0",
    "params": {
        "model": "res.partner",
        "method": "web_read",
        "args": [[46]],
        "kwargs": {
            "specification": {
                "bank_ids": {
                    "fields": {
                        "acc_holder_name": {},
                        "acc_number": {},
                        "allow_out_payment": {},
                        "bank_id": {
                            "fields": {
                                "display_name": {}
                            }
                        },
                        "sequence": {}
                    },
                    "limit": 40,
                    "order": "sequence ASC, id ASC"
                }
            }
        }
    }
}
```

### web_search_read (list)

list ကို တောင်းယူလိုလျှင် `web_search_read` ကို အသုံးပြုနိုင်ပါသည်။

```json 
// {{host}}/web/dataset/call_kw
{
    "jsonrpc": "2.0",
    "params": {
        "model": "res.partner",
        "method": "web_search_read",
        "args": [],
        "kwargs": {
            "count_limit": 10001,
            "domain": [],
            "limit": 1,
            "offset": 0,
            "order": "id desc",
            "specification": {
                "category_id": {
                    "fields": {
                        "color": {},
                        "display_name": {}
                    }
                },
                "display_name": {},
                "email": {},
                "write_date": {}
            }
        }
    }
}
```

### call_button ( execute method)
model ထဲမှ method တွေကို execute ပြုလုပ်လိုလျှင် `call_button` ကို အသုံးပြုနိုင်ပါသည်။
```json
// {{host}}/web/dataset/call_button
{
    "jsonrpc":"2.0",
    "params":{
        "method":"create_invoices",
        "model":"sale.advance.payment.inv",
        "args":[[2], {"advance_payment_method": "delivered", "amount": 100}],
        "kwargs":{}
    }
}
```