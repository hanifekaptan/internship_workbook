package table1;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.sql.Timestamp;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.concurrent.ThreadLocalRandom;


/*
 * Hedef: 1 milyon satırdan meydana gelen bir tablo oluşturmak
 * 
 * Tabloda yer alacak değişkenler:
 * ID: integer türünde unique bir sayı
 * TamSayi1: 0 ile 10 milyon arasında random bir tam sayı
 * TamSayi2: -10 milyon ile +10 milyon arasında random bir tam sayı
 * GaussianTamSayi1: mean=0, variance=1 milyon olacak şekilde gaussian tam sayı
 * GaussianReelSayi1: mean=0, variance=1 milyon olacak şekilde gaussian reel sayı, sondaki decimal kısımdan random (5) digit bırak
 * GaussianReelSayi2: mean=0.5, variance=1 olacak şekilde gaussian reel sayı, sondaki decimal kısımdan random (5) digit bırak diğerlerini at
 * GaussianDate1: mean=0, variance=10000 olacak şekilde gaussian reel sayı üret, bu güne göre date'e çevir, sadece gün kısmını bırak
 * GaussianDate2: mean=0, variance=1000 olacak şekilde gaussian reel sayı üret, günü 01.01.1990'a ekle, saniyeye kadar çevir
 * GaussianDate3: mean=0, variance=10 olacak şekilde gaussian reel sayı üret, bu güne ekle, timestamp'e çevir
 * Binary1: mean=128, variance=100 olacak şekilde Random(2-50) gaussian reel sayı üret, HEX'e çevir, birleştir ve string olarak kaydet.
 * 
 * */


public final class DataGenerator {

    private static final LocalDate BASE_DATE_1990 = LocalDate.of(1990, 1, 1);

    private DataGenerator() {}

    public static DataRow createRow() {
        return new DataRow(
	            generateTamSayi(0, Config.TAMSAYI_RANGE),
	            generateTamSayi(-Config.TAMSAYI_RANGE, Config.TAMSAYI_RANGE),
	            generateGaussianTamSayi(Config.GAUSSIAN_MEAN_0, Config.STD_DEV_1M),
	            generateGaussianReelSayi(Config.GAUSSIAN_MEAN_0, Config.STD_DEV_1M, 5, RoundingMode.HALF_UP),
	            generateGaussianReelSayi(Config.GAUSSIAN_MEAN_0_5, Config.STD_DEV_1, 5, RoundingMode.DOWN),
	            generateGaussianDate(Config.GAUSSIAN_MEAN_0, Config.STD_DEV_10K, LocalDate.now()),
	            generateGaussianDateTime(Config.GAUSSIAN_MEAN_0, Config.STD_DEV_1K, BASE_DATE_1990),
	            generateGaussianTimestamp(Config.GAUSSIAN_MEAN_0, Config.STD_DEV_10, LocalDate.now()),
	            generateBinary(Config.BINARY_MEAN, Config.BINARY_STD_DEV, 2, 50)
        );
    }

    private static int generateTamSayi(int start, int end) {
    	return ThreadLocalRandom.current().nextInt(start, end);
    }
    
    private static double generateGaussianReelSayi(double mean, double std_dev) {
    	return ThreadLocalRandom.current().nextGaussian(mean, std_dev);
    }
    
    private static int generateGaussianTamSayi(double mean, double std_dev) {
        return (int) Math.round(generateGaussianReelSayi(mean, std_dev));
    }
    
    private static double generateGaussianReelSayi(double mean, double std_dev, int scale, RoundingMode mode) {
    	double gaussianSayi = generateGaussianReelSayi(mean, std_dev);
		return new BigDecimal(gaussianSayi).setScale(scale, mode).doubleValue();
    }
    
    private static LocalDate generateGaussianDate(double mean, double std_dev, LocalDate date) {
    	long daysToAdd = (long) generateGaussianReelSayi(mean, std_dev);
    	return date.plusDays(daysToAdd);
    }
    
    private static LocalDateTime generateGaussianDateTime(double mean, double std_dev, LocalDate date) {
        long daysToAdd = (long) generateGaussianReelSayi(mean, std_dev);
        LocalDateTime randomDateTime = date.plusDays(daysToAdd).atStartOfDay();
        // saat-dakika-saniye kısmı rastgele üretilecekse aşağıdaki kodlar kullanılabilir
        // long randomSecondsInDay = ThreadLocalRandom.current().nextLong(86400);
        // randomDateTime = randomDateTime.plusSeconds(randomSecondsInDay);
        return randomDateTime;
    }

    private static Timestamp generateGaussianTimestamp(double mean, double std_dev, LocalDate date) {
    	LocalDateTime randomDateTime = generateGaussianDateTime(mean, std_dev, date);
        return Timestamp.valueOf(randomDateTime);
    }
    
    private static String generateBinary(double mean, double std_dev, int min, int max) {
    	int numberOfGaussians = generateTamSayi(min, max);
    	ArrayList<String> hexList = new ArrayList<>(numberOfGaussians);
        for (int i = 0; i < numberOfGaussians; i++) {
            double gaussianValue = generateGaussianReelSayi(mean, std_dev);
            hexList.add(Double.toHexString(gaussianValue));
        }
        return String.join("", hexList);
    }
}