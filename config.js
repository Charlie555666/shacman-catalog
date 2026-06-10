/*  SHACMAN Catalog — 全局配置文件
 *  编辑此文件后，所有页面自动生效，无需重新生成 HTML
 */

// ── Google Apps Script Web App 地址（由你部署后粘贴） ─────────
var APPS_SCRIPT_URL = '';
// 示例: 'https://script.google.com/macros/s/xxxxxxx/exec'

// ── 下载登录弹窗文案（可按国家覆盖）────────────────────────────
var DL_LABELS = {
  'zh': {
    title:   '下载产品规格书',
    hint:   '请填写信息后下载，方便我们为您提供更精准的服务',
    name_ph: '姓名 / Name',
    phone_ph:'手机号 / Phone',
    company_ph:'公司名称 / Company',
    cancel:  '取消',
    submit:  '提交并下载',
    alert:   '请填写姓名和手机号'
  },
  'en': {
    title:   'Download Spec Sheet',
    hint:   'Please fill in your details to download',
    name_ph: 'Name',
    phone_ph:'Phone',
    company_ph:'Company',
    cancel:  'Cancel',
    submit:  'Submit & Download',
    alert:   'Please fill in name and phone'
  }
};
