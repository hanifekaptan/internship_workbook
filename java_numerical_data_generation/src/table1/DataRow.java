package table1;

import java.sql.Timestamp;
import java.time.LocalDate;
import java.time.LocalDateTime;

public record DataRow(
	    int tamSayi1,
	    int tamSayi2,
	    int gaussianTamSayi1,
	    double gaussianReelSayi1,
	    double gaussianReelSayi2,
	    LocalDate gaussianDate1,
	    LocalDateTime gaussianDate2,
	    Timestamp gaussianDate3,
	    String binary1
) {}
