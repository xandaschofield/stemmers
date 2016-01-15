
import java.io.*;
import java.util.zip.*;

public class VariationOfInformation {

	public static double getVOI(File leftFile, File rightFile, int numTopics) throws Exception {
		BufferedReader leftReader =
			new BufferedReader(new InputStreamReader(new GZIPInputStream(new FileInputStream(leftFile))));

		BufferedReader rightReader =
			new BufferedReader(new InputStreamReader(new GZIPInputStream(new FileInputStream(rightFile))));
		
		System.err.println(leftFile + " " + rightFile + " " + numTopics);

		String leftLine, rightLine;
		
		double voi = 0;

		int[] leftCounts = new int[numTopics];
		int[] rightCounts = new int[numTopics];
		int[][] leftRightCounts = new int[numTopics][numTopics];
		int totalTokens = 0;
		
		while ((leftLine = leftReader.readLine()) != null) {
			if (leftLine.startsWith("#")) { continue; }

			// This could null pointer if right is shorter than left...
			rightLine = rightReader.readLine();
			while (rightLine.startsWith("#")) {
				rightLine = rightReader.readLine();
			}

			String[] leftFields = leftLine.split(" ");
			String[] rightFields = rightLine.split(" ");

			int leftTopic = Integer.parseInt(leftFields[5]);
			int rightTopic = Integer.parseInt(rightFields[5]);

			leftCounts[leftTopic]++;
			rightCounts[rightTopic]++;
			leftRightCounts[leftTopic][rightTopic]++;
			totalTokens++;
		}

		leftReader.close();
		rightReader.close();

		return getEntropy(leftCounts, totalTokens) +
			getEntropy(rightCounts, totalTokens) -
			2 * getMutualInformation(leftCounts, rightCounts, leftRightCounts, totalTokens);
	}

	public static double getEntropy(int[] counts, int total) {
		double entropy = 0.0;
		
		for (int i=0; i<counts.length; i++) {
			if (counts[i] > 0) {
				double p = (double) counts[i] / total;
				entropy -= p * Math.log(p);

				if (Double.isNaN(entropy)) {
					System.out.println("NaN: " + counts[i] + " / " + total);
				}
			}
		}

		return entropy;

	}

	public static double getMutualInformation(int[] leftCounts, int[] rightCounts, int[][] leftRightCounts, int total) {
		
		double mutualInformation = 0.0;

		for (int i = 0; i < leftCounts.length; i++) {
			if (leftCounts[i] > 0) {
				double p = (double) leftCounts[i] / total;
				for (int j = 0; j < rightCounts.length; j++) {
					if (leftRightCounts[i][j] > 0) {
						double joint = (double) leftRightCounts[i][j] / total;
						double q = (double) rightCounts[j] / total;

						mutualInformation += joint * Math.log(joint / (p * q));
					}
				}
			}
		}

		return mutualInformation;
	}

	public static void main (String[] args) throws Exception {
		int numTopics = Integer.parseInt(args[0]);
		int numFiles = args.length - 1;

		double[][] scores = new double[ numFiles ][ numFiles ];

		for (int i = 0; i < numFiles - 1; i++) {
			for (int j = i + 1; j < numFiles; j++) {
				double score = getVOI( new File(args[i+1]), new File(args[j+1]), numTopics);

				scores[i][j] = score;
				scores[j][i] = score;

				System.out.println(args[i + 1] + "\t" + args[j + 1] + "\t" + score);				
			}
		}

		/*
		for (int col = 0; col < numFiles; col++) {
			System.out.print(args[col] + "\t");
		}
		System.out.println();

		for (int row = 0; row < numFiles; row++) {
			for (int col = 0; col < numFiles; col++) {
				System.out.print(scores[row][col] + "\t");
			}
			System.out.println();
		}
		*/
		
	}
	
}
