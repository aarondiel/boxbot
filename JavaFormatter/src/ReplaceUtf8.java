import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;

class ReplaceUtf8 {
	static void replace(InputStream input) {
		try {
			for (
				int character = input.read();
				character != -1;
				character = input.read()
			) {
				if (0x00 <= character && character <= 0x7f)
					System.out.print((char)character);
				else
					System.out.print(String.format("\\u%04x", character));
			}

			input.close();
		} catch (IOException e) {}
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
			System.out.printf("no such file \"%s\"%n", args[0]);
			System.exit(1);
		}

		replace(input);
	}
}
