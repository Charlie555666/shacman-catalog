// CloudBase submit proxy - loaded as script to bypass risk warning
(function() {
  var CLOUDBASE_ENV = 'gengyanchao-d0gyzofwr69907e3c';
  var CALLBACK_PARAM = 'cb';

  var params = {};
  var src = document.currentScript ? document.currentScript.src : '';
  if (!src && document.scripts) {
    var scripts = document.scripts;
    src = scripts[scripts.length - 1].src;
  }

  (src.split('?')[1] || '').split('&').forEach(function(p) {
    var pair = p.split('=');
    if (pair[0] && pair[0] !== CALLBACK_PARAM) {
      params[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1] || '');
    }
  });

  var cbName = (src.match(/[?&]cb=([^&]+)/) || [])[1];

  if (!params.name || !params.phone) {
    if (cbName && window[cbName]) window[cbName]({code:-1,msg:'Missing params'});
    return;
  }

  try {
    var app = cloudbase.init({ env: CLOUDBASE_ENV, region: 'ap-shanghai' });
    var db = app.database();

    app.auth({ persistence: 'local' })
      .anonymousAuthProvider()
      .signIn()
      .then(function() {
        return db.collection('pdf_downloads').add({
          name: params.name,
          phone: params.phone,
          company: params.company || '',
          country: params.country || '',
          model: params.model || '',
          pageUrl: params.ref || '',
          createdAt: new Date().toISOString()
        });
      })
      .then(function(res) {
        if (cbName && window[cbName]) window[cbName]({code:0,id:res.id});
      })
      .catch(function(err) {
        if (cbName && window[cbName]) window[cbName]({code:-1,msg:err.message||String(err)});
      });
  } catch(e) {
    if (cbName && window[cbName]) window[cbName]({code:-1,msg:e.message});
  }
})();
