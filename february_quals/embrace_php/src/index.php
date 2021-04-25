<?php

if (isset($_REQUEST['login_data'])) {
    $json = @json_decode($_REQUEST['login_data']);
    if (!is_array($json) || count($json) < 2)
        exit('Error Json need to have 2 elements!');
    $json = array_values($json);
    list($login, $password) = $json;

    if (
        $login == 'admin' &
        $password == getenv('ADMIN_PASSW')
    )
        $_SESSION['isAdmin'] = true;
    else
        $_SESSION['isAdmin'] = false;
}
?>

<main role="main" class="inner cover">
    <div>
    <h1 class="cover-heading">Login Page</h1>
    <p class="lead">
        <?php
        if (isset($_SESSION['isAdmin']) && $_SESSION['isAdmin']) {
            ?>
            <p>Success YOURa ADMIN!!01!</p>
            <p>Your flag: <?=getenv('FLAG');?></p>
            <?php
        } else {
            if (isset($_REQUEST['login_data']))
            {
                ?>
                <p>Invalid login/password</p>
                <?php
            }
            ?>
            <form method=GET onsubmit="login_data.value = JSON.stringify([ inputLogin.value, inputPassword.value ]);">
                <input type="hidden" id="login_data" name="login_data" value="[false, false]">
                <p>
                    <label for="inputLogin" class="sr-only">Login</label>
                    <input
                    type="text"
                    id="inputLogin"
                    class="form-control"
                    value="<?=(isset($login) ? htmlspecialchars($login, ENT_QUOTES) : '')?>"
                    placeholder="Login"
                    required>
                </p>
                <p>
                    <label for="inputPassword" class="sr-only">Password</label>
                    <input type="password" id="inputPassword" class="form-control" placeholder="Password" required>
                </p>
                <p>
                    <button class="btn" type="submit">Sign in</button>
                </p>
            </form>
            <?php
        }
        ?>
    </p>
    </div>
</main>