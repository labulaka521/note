# Golang编译器

**Golang的编译器入口**

Golang的编译器入口在`src/cmd/compile/internal/gc/main.go` 文件的`func Main(archInit func(*Arch))`函数中，这个函数先会获取命令行的参数并且修改编译的选项配置，然后运行`loadsys`加载底层的函数，然后运行`parseFiles`函数对所有输入的文件进行词法和语法分析 得到对应的抽象语法树(AST)，然后就开始了九个阶段来对生成的语法树变形更新与编译

- Phase 1: const, type, and names and types of funcs.
- Phase 2: Variable assignments.
- Phase 3: Type check function bodies.
- Phase 4: Decide how to capture closed variables.
- Phase 5: Inlining(检查内联函数的类型)
- Phase 6: Escape analysis.(逃逸分析)
- Phase 7: Transform closure bodies to properly reference captured variables.
- Phase 8: Compile top level functions.
- Phase 9: Check external declarations.

