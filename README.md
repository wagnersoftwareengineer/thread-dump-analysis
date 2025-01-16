# Doc Análise das Threads

## 1. Comentários Iniciais
Este documento apresenta a análise de performance realizada a partir de dumps de threads coletados de um serviço em produção. O objetivo é identificar gargalos de execução que levam à degradação de performance e propor soluções para mitigar o problema.

## 2. Diagnóstico do Problema
A análise revelou um aumento significativo de threads em estado `WAITING` ou `BLOCKED` durante o horário de maior carga. O gráfico de threads `RUNNABLE` mostrou um crescimento repentino, seguido por uma queda , indicando possíveis contenções de recursos compartilhados.

### **Gráficos Gerados**
- **Threads em `WAITING/BLOCKED`**: Mostra o crescimento de threads aguardando acesso a um recurso.
- **Threads `RUNNABLE`**: Indica que o serviço processa múltiplas requisições simultaneamente.

---

## 3. Pesquisas e Referências Utilizadas
Para entender melhor as possíveis causas e soluções, realizei pesquisas em documentações oficiais e fóruns técnicos:
- [Documentação do Java sobre `Thread States`](https://docs.oracle.com/javase/tutorial/essential/concurrency/)
- [Threads em microsserviços](https://www.baeldung.com/java-concurrency-locks)
- Discussões em fóruns como **Stack Overflow** sobre melhores práticas de uso de `synchronized`, `ThreadPoolExecutor` e `ReentrantLock`.
  
### **Insights Obtidos nas Pesquisas**
- Threads `WAITING` indicam espera em monitores, filas ou operações assíncronas.
- Utilizar caches pode reduzir a quantidade de chamadas repetitivas que causam bloqueios.
- `ThreadPoolExecutor` deve ser ajustado conforme a carga esperada para evitar sobrecarga ou ociosidade.

---

## 4. Soluções Propostas

### **1. Revisão de Código para Concorrência**
- Verificar métodos que utilizam `synchronized` para reduzir pontos de bloqueio.
- Utilizar `ReentrantLock` com timeout para evitar travamentos indefinidos.

### **2. Pool de Conexões e Cache**
- Implementar um **pool de conexões** para bancos de dados e serviços externos.
- Utilizar um **cache de respostas** para evitar chamadas repetitivas.

### **3. Monitoramento em Tempo Real**
- Adicionar métricas de monitoramento para alertar quando as threads em `WAITING`/`BLOCKED` excederem um limite crítico.

---

## 5. Sugestão para Plano de Ação
1. Possibilidade para implementar logs detalhados para identificar pontos críticos de bloqueio.
2. Conferir a possibilidade de Testar as soluções em um ambiente de homologação com carga simulada.
3. Se ocorrer ajustes, avaliar novamente.
