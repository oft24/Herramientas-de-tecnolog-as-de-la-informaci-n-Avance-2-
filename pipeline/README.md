# Pipeline de calidad

El pipeline ejecuta controles relacionados con los riesgos de esta aplicación y termina en una sola decisión:

```powershell
python pipeline/run_pipeline.py
```

Para generar la evidencia roja de una credencial detectada:

```powershell
python pipeline/run_pipeline.py --demo-red *> reportes/corrida_roja.txt
python pipeline/run_pipeline.py *> reportes/corrida_verde.txt
```

El modo rojo crea un candidato temporal con una asignación de secreto, lo inspecciona y lo elimina al terminar. No se guarda ninguna credencial en el repositorio.
