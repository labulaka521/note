# Sscan vs Sscanf vs Sscanln的示例

- Sscan扫描参数字符串，将连续的空格分隔值存储到连续的参数中。换行计为空格。
- Sscanf扫描参数字符串，将连续的空格分隔值存储到由格式确定的连续参数中。
- Sscanln类似于Sscan，但在新行停止扫描，在最终项目之后必须有换行符或EOF。


```
package main
 
import (
    "fmt"      
)
 
func main(){    
    var X int
    var Y int
 
    fmt.Printf("\nIntital X: %d, Y: %d", X, Y)
 
    fmt.Sscan("100\n200", &X, &Y)
    fmt.Printf("\nSscan X: %d, Y: %d", X, Y)
 
    fmt.Sscanf("(10, 20)", "(%d, %d)", &X, &Y)
    fmt.Printf("\nSscanf X: %d, Y: %d", X, Y)
     
    fmt.Sscanln("50\n50", &X, &Y)
    fmt.Printf("\nSscanln X: %d, Y: %d", X, Y)
}
```
