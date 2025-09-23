public class UserService {
    public void connectDB() {
        String url = "jdbc:mysql://localhost:3306/userdb?user=admin&password=123456";
        Connection conn = DriverManager.getConnection(url);
        // 未关闭连接
    }

    public void logUser(User user) {
        System.out.println("用户登录: " + user.getPassword()); // 打印密码
    }
}