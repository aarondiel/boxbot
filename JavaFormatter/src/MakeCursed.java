import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

class MakeCursed {
	static int get_longest_line(InputStream input, StringBuilder builder) {
		Scanner scanner = new Scanner(input);
		int longest_line = 0;

		while (scanner.hasNextLine()) {
			String line = scanner.nextLine();

			builder.append(line.toString());
			builder.append(System.lineSeparator());
			longest_line = Math.max(line.length(), longest_line);
		}

		scanner.close();

		return longest_line;
	}

	static void replace(String input, int longest_line) {
		longest_line = Math.max(76, longest_line) + 2;

		// seperate clauses like "} else" or "} catch" into two seperate lines
		Matcher pattern = Pattern.compile("(\s*)} (\\w+)(.*)$", Pattern.MULTILINE)
			.matcher(input);

		while (pattern.find()) {
			String replace_string = pattern.group(1) +
				"}\n" +
				pattern.group(1) +
				pattern.group(2) +
				pattern.group(3);

			input = input.replace(pattern.group(0), replace_string);
		}

		// join "}" with line before it
		input = input.replaceAll("\\s*}", " }");

		// pad every ";" and " {" to the end of the line
		pattern = Pattern.compile("(.*)(;| \\{)(\\W*)$", Pattern.MULTILINE)
			.matcher(input);

		while (pattern.find()) {
			String start = pattern.group(1);
			String delimiter = pattern.group(2).equals(" {") ? " {" : " ;";
			String end = pattern.group(3);

			String spacing = " ".repeat(longest_line - start.length());

			input = input.replace(
				pattern.group(0),
				start + spacing + delimiter + end
			);
		}

		System.out.print(input);
	}

	static InputStream open_file(String path) {
		try {
			return new FileInputStream(path);
		} catch (FileNotFoundException e) { }

		return null;
	}

	public static void main(String[] args) {
		InputStream input = args.length == 0 ?
			System.in :
			open_file(args[0]);

		if (input == null) {
			System.out.println("file not found");
			System.exit(1);
		}
			
		StringBuilder builder = new StringBuilder();
		int longest_line = get_longest_line(input, builder);
		replace(builder.toString(), longest_line);
	}
}
