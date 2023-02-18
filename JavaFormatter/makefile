all: bin/MakeCursed.jar bin/ReplaceTabs.jar bin/ReplaceUtf8.jar

build/%.class: src/%.java
	@mkdir -p build
	@javac -d build $<

bin/%.jar: build/%.class
	@echo "Main-class: " $(shell basename -s ".class" $<) > build/manifest.mf
	@mkdir -p bin
	@(cd build && jar cmf manifest.mf ../$@ $(shell basename $<))

.PHONY: clean
clean:
	@rm -rf build bin
