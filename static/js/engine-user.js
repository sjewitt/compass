var engine = {

    // pass in loaded data here 
    init: function (display_data) {
        let btn_add_user = document.getElementById("btn_add_user");
        if (btn_add_user) {
            btn_add_user.addEventListener("click", this.submitNewUserDataHandler)
        }

        let btn_update_user = document.getElementById("btn_update_user");
        if (btn_update_user) {
            btn_update_user.addEventListener("click", this.submitUpdateUserDataHandler)
        }
    },

    submitNewUserDataHandler: function () {
        let submit = true;
        /** Note: A NEW user will not have Competencies. Handle the null/empty array at the back-end */
        data = {}
        // data['id'] = document.getElementById("user_id").value;  // -1 if new user
        data['username'] = document.getElementById("new_user_login").value;
        data['compass_id'] = document.getElementById("compass_id").value;
        data['name'] = document.getElementById("new_user_name").value;
        data['email'] = document.getElementById("new_user_email").value;
        data['password'] = document.getElementById("new_user_pwd").value;
        data['password_check'] = document.getElementById("new_user_pwd_repeat").value;
        if (data["password"] !== data["password_check"]) {    // also checks on server
            submit = false;
        }
        console.table(data);
        
        // TODO: Do blur/change handlers and alert in real-time 
        if (submit) {
            fetch('/users/new/', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            }).then(function (response) {
                return response.json();
            }).then(function (response) {
                /** the ResponseRedirect from the server is failing, so
                 * try with JS instead:
                 */
                if (response.usercreated) {
                    document.location.href = `/${response.user_id}`
                }
            });
        }
    },

    submitUpdateUserDataHandler: function () {
        let submit = true;
        data = {}
        data['username'] = document.getElementById("update_user_login").value;
        data['id'] = parseInt(document.getElementById("update_user_id").value);
        data['compass_id'] = parseInt(document.getElementById("compass_id").value);
        data['name'] = document.getElementById("update_user_name").value;
        data['email'] = document.getElementById("update_user_email").value;
        /** 
         * TODO: check if pwds are present, then are the same, then match existing pwd 
         * This needs to call a back-end check so we don't have the old pwd on
         * client...
        */
        // if(data["password"] !== data["password_check"]){    // also checks on server
        //     submit = false;
        // }
        // TODO: Do blur/change handlers and alert in real-time 
        if (submit) {
            fetch(`/users/${data['id']}/edit/`, {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            }).then(function (response) {
                return response.json();
            }).then(function (response) {
                /** the ResponseRedirect from the server is failing, so
                 * try with JS instead:
                 */
                if (response.username) {  // check that it is a User object
                    document.location.href = `/${response.id}/`
                }
                else {
                    // render a message - wrong user ID etc
                    elem = document.getElementById("message")
                    elem.innerHTML = "Error"
                }
            });
        }
    },
};

document.addEventListener("DOMContentLoaded",
    (evt) => {
        // if we are not `fetch()`ing, just call `init()` here:
        engine.init(null);
    }
)