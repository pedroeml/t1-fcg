## Logs de eventos:
- aproximação
- afastamento
- criação de grupo com uma unica pessoa (Group created)
- criação de grupo com mais de uma pessoa (Group updated)
- join de uma ou mais pessoas em um grupo já existente
- left de uma ou mais pessoas em um grupo já existente

## Visualização:
- grouping, pela cor (view de imagem e de mundo)
- tracking, pelos pontos (view de mundo)

## Vídeos testados:
- BR-01
- BR-07
- UKN-01
- UKN-03
- AT-01
- AT-02
- CN-01
- CN-02

Em alguns vídeos percebe-se que as coordenadas de mundo estão um tanto estranhas na visualização!
- BR-07
A camera (imagem e mundo) está num ângulo estranho (mas não compromete a detecção de eventos:
- AT-01

### TooFarDistance:
Distância máxima que define se é necessário verificar evento de aproximação/afastamento
- 400	(BR-01) Um valor exageradamente alto, pessoas que estavam em lados opostos da imagem eram indentificados eventos de aproximação, o que gerava spamming no logging dos eventos.
- 300 	(BR-01) Em comparação com 4 m consideravelmente o número de eventos disparados, mas muitos dos logs exibidos ainda parecem desnecessários.
- 250	(BR-01) Este é um bom valor pois 2,5 m é uma distância interessante de avaliar aproximação ou distanciamento entre pessoas, além de diminuir muito os logs.

### MinimumDistanceChange:
Distancia mínima de variação entre duas pessoas em 3 frames de diferença para verificar evento de aproximação/afastamento
- 5		(BR-01) É um valor muito baixo para uma variação de distância, exibe muitos logs, porém estes condizem com a realidade
- 7		(BR-01) É um valor razoável e permite desconsiderar mudanças mínimas
- 15 	(BR-01) Com poucas pessoas e no início do vídeo geralmente nenhum evento é disparado

### GroupingMaxDistance:
Distância máxima entre duas pessoas que podem serem consideradas um grupo
- 100	(BR-01) Nota-se que há casos em que um par de pessoas estão andando lado a lado e são classificadas como em grupos distintos.
- 120	(UKN-01) Parece um valor razoável os agrupamentos na visualização
- 150	(BR-01) Com esta distância o problema anterior não ocorre mais, mas há casos em que visualizando o vídeo uma pessoa que nem parece estar tão próxima acaba acidentalmente incluída no grupo. 
		(BR-07) (UKN-01) No entanto, pessoas que estavam exatamente uma do lado da outra acabavam  sendo consideradas grupos diferentes. 
