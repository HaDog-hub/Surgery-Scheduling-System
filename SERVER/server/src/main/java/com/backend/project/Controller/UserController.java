package com.backend.project.Controller;

import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.backend.project.Service.UserService;
import com.backend.project.model.User;

@CrossOrigin(origins = { "*" })
@RestController
@RequestMapping("/api")
public class UserController {

    @Autowired
    private UserService userService;

    @Autowired
    private JavaMailSender mailSender;

    // ???餃
@PostMapping("/login")
public ResponseEntity<?> login(@RequestBody User user) {
    try {
        System.out.println("===== ?嗅?餃隢? =====");
        System.out.println("?嗅??User ?拐辣: " + user);
        System.out.println("User ?臬??null: " + (user == null));
        
        if (user != null) {
            System.out.println("?嗅?董?? [" + user.getUsername() + "]");
            System.out.println("撣唾??臬??null: " + (user.getUsername() == null));
        }
        
        User authenticate = userService.authenticate(user.getUsername(), user.getPassword());
        
        if (authenticate != null) {
            System.out.println("===== ?餃?? =====");
            System.out.println("雿輻???? " + authenticate.getUsername() + " - " + authenticate.getName());
            return ResponseEntity.ok("?餃??");
        } else {
            System.out.println("===== ?餃憭望?嚗董??撖Ⅳ?航炊 =====");
            return ResponseEntity.ok("*撣唾???蝣潮隤?);
        }
    } catch (Exception e) {
        System.err.println("===== ?餃??隤?=====");
        e.printStackTrace();
        return ResponseEntity.status(500).body("?餃憭望?: " + e.getMessage());
    }
}

    @PostMapping("/login/sendVerificationCode")
    public ResponseEntity<?> sendVerificationCode(@RequestBody User user) {
        User foundUser = userService.forgotPasswordAuthenticate(user.getUsername(), user.getEmail());
        if (foundUser == null) {
            return ResponseEntity.badRequest().body("撣唾??摮隞園隤?);
        }

        String toEmail = foundUser.getEmail();
        if (toEmail == null || !toEmail.matches("^[\\w.-]+@[\\w.-]+\\.[A-Za-z]{2,6}$")) {
            return ResponseEntity.badRequest().body("Email ?澆??航炊嚗?);
        }

        String code = userService.generateVerificationCode();
        userService.saveVerificationCode(foundUser, code);

        try {
            SimpleMailMessage message = new SimpleMailMessage();
            message.setTo(toEmail);
            message.setSubject("??賣?銵?蝔恣?頂蝯勗?蝣潮?蝵桅?霅Ⅳ??);
            message.setText("閬芣??蝙?刻憟踝?\n\n?函隢?撖Ⅳ?蔭?n\n?函?撽?蝣潭嚗?" + code +
                    "\n\n隢 5 ???找蝙?冽迨撽?蝣澆???雿n\n?仿??冽鈭箸?雿?隢蕭?交迨靽～n\nMedTime 蝟餌絞?砌?");

            mailSender.send(message);
            return ResponseEntity.ok("撽?蝣澆歇?潮?函?靽∠拳");
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(500).body("?潮隞嗅仃??隢?敺?閰?);
        }
    }

    @PostMapping("/login/verifyCode")
    public ResponseEntity<?> verifyCode(@RequestBody Map<String, String> payload) {
        String username = payload.get("username");
        String email = payload.get("email");
        String inputCode = payload.get("verificationCode");

        User authenticate = userService.forgotPasswordAuthenticate(username, email);
        if (authenticate == null) {
            return ResponseEntity.badRequest().body("撣唾??摮隞園隤?);
        }

        if (!userService.verifyCode(authenticate, inputCode)) {
            return ResponseEntity.badRequest().body("撽?蝣潮隤斗?撌脤???);
        }

        userService.clearVerificationCode(authenticate);
        return ResponseEntity.ok("撽???");
    }

    @PostMapping("/login/ForgotPassword")
    public String forgotPassword(@RequestBody User user) {
        User authenticate = userService.forgotPasswordAuthenticate(user.getUsername(), user.getEmail());
        return (authenticate != null) ? "1" : "*撣唾??摮隞園隤?;
    }

    @PutMapping("/login/changePassword/{username}")
    public ResponseEntity<String> changePassword(@PathVariable String username, @RequestBody User user) {
        String result = userService.changePassword(username, user.getPassword());
        if ("Change Password successfully".equals(result)) {
            return ResponseEntity.ok(result);
        } else {
            return ResponseEntity.status(404).body(result);
        }
    }

    @GetMapping("/system/users")
    public ResponseEntity<?> getAllUsers() {
        try {
            System.out.println("===== [Controller] ???脣???蝙?刻?=====");
            List<User> users = userService.getAllUsers();
            System.out.println("===== [Controller] ???脣? " + users.size() + " ?蝙?刻?=====");
            
            // ?啣蝚砌??蝙?刻?閮?瑼Ｘ
            if (!users.isEmpty()) {
                User firstUser = users.get(0);
                System.out.println("蝚砌??蝙?刻? " + firstUser.getUsername() + ", " + firstUser.getName());
            }
            
            return ResponseEntity.ok(users);
        } catch (Exception e) {
            System.err.println("===== [Controller] ?航炊?潛? =====");
            System.err.println("?航炊憿?: " + e.getClass().getName());
            System.err.println("?航炊閮: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(500).body("?脣?雿輻??銵典仃?? " + e.getMessage());
        }
    }

    @GetMapping("/system/user/{username}")
    public User getUser(@PathVariable String username) {
        return userService.getUser(username);
    }

    @PutMapping("/system/user/{username}")
    public ResponseEntity<?> updateUser(@PathVariable String username, @RequestBody User updatedUser) {
        userService.updateUser(username, updatedUser);
        return ResponseEntity.ok("User update successfully");
    }

    @PostMapping("/system/user/add")
    public ResponseEntity<?> addUser(@RequestBody User user) {
        userService.addUser(user);
        return ResponseEntity.ok("User add successfully");
    }

    @PostMapping("/system/users/add")
    public ResponseEntity<?> addUsers(@RequestBody List<User> users) {
        userService.addUsers(users);
        return ResponseEntity.ok("Users add successfully");
    }

    @DeleteMapping("/system/user/delete/{username}")
    public ResponseEntity<?> deleteUser(@PathVariable String username) {
        userService.deleteUser(username);
        return ResponseEntity.ok("User deleted successfully");
    }

    @DeleteMapping("/system/users/delete")
    public ResponseEntity<?> deleteUsers(@RequestBody List<String> usernames) {
        userService.deleteUsers(usernames);
        return ResponseEntity.ok("Users deleted successfully");
    }
}
