import os
import json
from flask import send_file, send_from_directory
from flask import Flask, render_template, request
from core import shterm_function
from conf import config

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    getShtermApi = shterm_function.shtermFunction(config.Server, config.ManagerID, config.ManagerPassword)
    data = {
        0: "用户账号与密码有效期延长成功",
        2: "有效期延长失败:未知的用户",
        3: "有效期延长失败:用户被禁用/锁定或者过期,请联系管理员处理",
        4: "有效期延长失败:密码不符合安全要求，要求长度至少为8个字符，同时包含数字、字母及字符",
        5: "有效期延长失败:用户OTP验证失败,请重试",
        9: "有效期延长失败:未知错误,请联系管理员处理"
    }
    if request.method == 'POST':
        user = request.form.get('username')
        otp = request.form.get('otp')
        verify_otp_res = json.loads(getShtermApi.verify_otp(user, otp))
        print(verify_otp_res)
        if verify_otp_res['code'] == 2000:
            getUserID = getShtermApi.getShtermUserID(user)
            getShtermApi.update_Password_ExpireTime(getUserID)
            getShtermApi.update_Account_ExpireTime(getUserID)
            return render_template('index.html', msg=data[0])
        elif verify_otp_res['code'] == 4003:
            return render_template('index.html', msg=data[2])
        elif verify_otp_res['code'] == 4011 and verify_otp_res['data'] == 3:
            return render_template('index.html', msg=data[3])
        elif verify_otp_res['code'] == 4011 and verify_otp_res['data'] == 5:
            return render_template('index.html', msg=data[5])
        else:
            return render_template('index.html', msg=data[9])
    else:
        return render_template('index.html')


@app.route("/download/<path:filename>", methods=['GET'])
def download(filename):
    dirpath = os.path.join(app.root_path, 'upload')
    return send_from_directory(dirpath, filename, as_attachment=True)


if __name__ == '__main__':
    app.run('0.0.0.0', ssl_context='adhoc')
