import sys
import os

class GenerateAst:
    def main(args):
        if len(args) != 1:
            print("Usage: generate_ast <output directory>", file=sys.stderr)
            sys.exit(64)

        outputDir = args[0]

        GenerateAst.define_ast(outputDir, "Expr", ("Assign : Token name, Expr value", 
            "Binary : Expr left, Token operator, Expr right", "Grouping : Expr expression", "Literal : Object value", 
            "Unary : Token operator, Expr right", "Variable : Token name"))
        GenerateAst.define_ast(outputDir, "Stmt", ["Block : List<Stmt> statements", "Expression : Expr expression", 
            "Print : Expr expression", "Var : Token name, Expr initializer"])

    def define_ast(outputDir, baseName, types):
        path = os.path.join(outputDir, f"{baseName}.java")

        with open(path, "w", encoding="utf-8") as writer:
            writer.write("package com.craftinginterpreters.lox;\n")
            writer.write("\n")
            writer.write("import java.util.List;\n")
            writer.write("\n")
            writer.write(f"abstract class {baseName} {{\n")
            writer.write("\n")
            writer.write("}\n")

            GenerateAst.defineVisitor(writer, baseName, types)
            
            for type in types:
                className = type.split(":")
                fields = type.split(":")
                className = className.strip()
                fields = fields.strip() 
                GenerateAst.defineType(writer, baseName, className, fields)
                writer.write()
                writer.write("  abstract <R> R accept(Visitor<R> visitor);")
                writer.write("    }")
                writer.write()
            writer.write("    @Override")
            writer.write("    <R> R accept(Visitor<R> visitor) {")
            writer.write("      return visitor.visit" + className + baseName + "(this);")
            writer.write("    }")

    def defineType(writer, baseName, className, fieldList):
        writer.write("  static class " + className + " extends " + baseName + " {")
        writer.write("    " + className + "(" + fieldList + ") {")
        fields = fieldList.split(", ")
        for field in fields:
            name = field.split(" ")[1]
            writer.write("      this." + name + " = " + name + ";")
        writer.write("    }")
        writer.write()
        for field in field:
            writer.write("    final " + field + ";")
        writer.write("  }")

    def defineVisitor(writer, baseName, types):
        writer.write("  interface Visitor<R> {")
        for type in types:
            typeName = type.split(":")[0].strip()
            writer.write("    R visit" + typeName + baseName + "(" + typeName + " " + baseName.lower() + ");")
        writer.write("  }")

if __name__ == "__main__":
    GenerateAst.main(sys.argv[1:])