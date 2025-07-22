package common;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.List;


public class DatabaseManager {

    private final String jdbcUrl;

    public DatabaseManager(String dbFileName) {
        this.jdbcUrl = "jdbc:sqlite:" + dbFileName;
    }

    @FunctionalInterface
    public interface RowBinder<T> {
        void bind(PreparedStatement ps, T row) throws SQLException;
    }

    public void createOrEnsureTable(String createTableSql) throws SQLException {
        try (Connection conn = DriverManager.getConnection(jdbcUrl);
        Statement stmt = conn.createStatement()) {
        	stmt.execute(createTableSql);
        }
    }

    public <T> void batchInsert(String insertSql, List<T> dataList, RowBinder<T> binder) throws SQLException {
        try (Connection conn = DriverManager.getConnection(jdbcUrl)) {
            conn.setAutoCommit(false);
            try (PreparedStatement ps = conn.prepareStatement(insertSql)) {
                for (T rowData : dataList) {
                    binder.bind(ps, rowData);
                    ps.addBatch();
                }
                ps.executeBatch();
                conn.commit();
            } catch (SQLException e) {
                conn.rollback();
                throw e;
            }
        }
    }
}