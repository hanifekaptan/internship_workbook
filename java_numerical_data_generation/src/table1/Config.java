package table1;

public final class Config {
    
    public static final String DB_FILE_NAME = "random_data.db";
    public static final String TABLE_NAME = "basic_data";
    
    public static final int ROW_COUNT = 1_000_000;
    public static final int BATCH_SIZE = 50_000;

    public static final int TAMSAYI_RANGE = 10_000_000;
    
    public static final double GAUSSIAN_MEAN_0 = 0.0;
    public static final double GAUSSIAN_MEAN_0_5 = 0.5;
    
    public static final double STD_DEV_1M = Math.sqrt(1_000_000);
    public static final double STD_DEV_1 = Math.sqrt(1);
    public static final double STD_DEV_10K = Math.sqrt(10000);
    public static final double STD_DEV_1K = Math.sqrt(1000);
    public static final double STD_DEV_10 = Math.sqrt(10);

    public static final double BINARY_MEAN = 128.0;
    public static final double BINARY_STD_DEV = Math.sqrt(100);
    public static final int BINARY_MIN_LENGTH = 2;
    public static final int BINARY_MAX_LENGTH = 50;

    private Config() {}
}