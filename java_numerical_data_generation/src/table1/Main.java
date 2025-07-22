// Main.java
package table1;

import common.DatabaseManager;
import java.sql.SQLException;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class Main {

    public static void main(String[] args) {
        System.out.println("Veri üretim ve veritabanına yazma işlemi başlıyor...");
        long startTime = System.currentTimeMillis();

        try {
            DatabaseManager dbManager = new DatabaseManager(Config.DB_FILE_NAME);
            String createTableSql = "CREATE TABLE IF NOT EXISTS " + Config.TABLE_NAME + " (\n"
                    + "    ID INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                    + "    TamSayi1 INTEGER NOT NULL,\n"
                    + "    TamSayi2 INTEGER NOT NULL,\n"
                    + "    GaussianTamSayi1 INTEGER NOT NULL,\n"
                    + "    GaussianReelSayi1 REAL NOT NULL,\n"
                    + "    GaussianReelSayi2 REAL NOT NULL,\n"
                    + "    GaussianDate1 TEXT NOT NULL,\n"
                    + "    GaussianDate2 TEXT NOT NULL,\n"
                    + "    GaussianDate3 TEXT NOT NULL,\n"
                    + "    Binary1 TEXT NOT NULL\n"
                    + ");";

            System.out.println("Veritabanı ve tablo oluşturuluyor/kontrol ediliyor...");
            dbManager.createOrEnsureTable(createTableSql);
            System.out.println("Tablo hazırlandı: " + Config.TABLE_NAME);

            String insertSql = "INSERT INTO " + Config.TABLE_NAME + 
                               " (TamSayi1, TamSayi2, GaussianTamSayi1, GaussianReelSayi1, GaussianReelSayi2, " +
                               "GaussianDate1, GaussianDate2, GaussianDate3, Binary1) VALUES (?,?,?,?,?,?,?,?,?)";

            DatabaseManager.RowBinder<DataRow> binder = (ps, row) -> {
                ps.setInt(1, row.tamSayi1());
                ps.setInt(2, row.tamSayi2());
                ps.setInt(3, row.gaussianTamSayi1());
                ps.setDouble(4, row.gaussianReelSayi1());
                ps.setDouble(5, row.gaussianReelSayi2());
                ps.setString(6, row.gaussianDate1().format(DateTimeFormatter.ISO_LOCAL_DATE));
                ps.setString(7, row.gaussianDate2().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
                ps.setString(8, row.gaussianDate3().toLocalDateTime().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
                ps.setString(9, row.binary1());
            };

            System.out.println("Toplam " + Config.ROW_COUNT + " satır veri üretilecek, " + Config.BATCH_SIZE + "'lik gruplar şeklinde ekleme yapılacak.");
            
            List<DataRow> dataBatch = new ArrayList<>(Config.BATCH_SIZE);
            int totalBatches = (int) Math.ceil((double) Config.ROW_COUNT / Config.BATCH_SIZE);

            for (int i = 0; i < Config.ROW_COUNT; i++) {
                dataBatch.add(DataGenerator.createRow());

                if (dataBatch.size() == Config.BATCH_SIZE || i == Config.ROW_COUNT - 1) {
                    dbManager.batchInsert(insertSql, dataBatch, binder);
                    
                    int currentBatchNumber = (i / Config.BATCH_SIZE) + 1;
                    System.out.println("Batch " + currentBatchNumber + "/" + totalBatches + " veritabanına yazıldı. (" + (i + 1) + " satır tamamlandı)");
                    
                    dataBatch.clear();
                }
            }

            long endTime = System.currentTimeMillis();
            long duration = endTime - startTime;

            System.out.println("\nİşlem Tamamlandı!");
            System.out.println("Toplam " + Config.ROW_COUNT + " satır veri '" + Config.DB_FILE_NAME + "' dosyasına yazıldı.");
            System.out.println("Geçen Süre: " + formatDuration(duration));

        } catch (SQLException e) {
            System.err.println("Veritabanı hatası oluştu: " + e.getMessage());
            e.printStackTrace();
        } catch (Exception e) {
            System.err.println("Başka bir hata oluştu: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    
    private static String formatDuration(long millis) {
        long minutes = TimeUnit.MILLISECONDS.toMinutes(millis);
        long seconds = TimeUnit.MILLISECONDS.toSeconds(millis) % 60;
        long remainingMillis = millis % 1000;
        return String.format("%d dakika, %d saniye, %d milisaniye", minutes, seconds, remainingMillis);
    }
}