# SISTEMA DE VIDEO COHERENTE v2.0 - Workflows

## 📁 WORKFLOWS CREADOS:

### WF0: character_pose_consistency_api.json ⭐ MÓDULO DE IDENTIDAD/POSE
**Propósito**: Generar el mismo personaje en una pose/situación específica (imagen fija) para crear anchors consistentes.
**VRAM**: ~6-8 GB (según resolución/steps)
**Input**:
- SCENE_PROMPT: Descripción de situación/encuadre
- POSE_IMAGE: Guía de pose (OpenPose o imagen de pose)
- REFERENCE_IMAGE: Imagen de identidad del personaje

**Output**:
- Imagen en: output/CharacterPose/

**Uso recomendado**:
- Crear “bible” del personaje antes de video (frontal, 3/4, perfil, acción, expresión, etc.)
- Reutilizar estos anchors en pipelines nuevos (Hunyuan/Wan) para continuidad visual

---

### WF1: pose_keyframe_generator.json
**Propósito**: Generar poses clave para guiar el movimiento
**VRAM**: ~4.2 GB (26%)
**Input**:
- POSE_DESCRIPTION: Descripción de la acción
- POSE_IMAGE: Imagen de referencia de pose (opcional)

**Output**:
- Imágenes de poses clave guardadas en: output/PoseGenerator/

**Tiempo**: 2-3 minutos por escena

---

### WF2: reference_image_generator.json
**Propósito**: Generar imagen de referencia del personaje
**VRAM**: ~5.6 GB (35%)
**Input**:
- CHARACTER_DESCRIPTION: Descripción del personaje

**Output**:
- Imagen de referencia guardada en: output/ReferenceGenerator/

**Tiempo**: 30 segundos por personaje

---

### WF3: coherent_video_generator.json ⭐ PRINCIPAL
**Propósito**: Generar video coherente usando ControlNet + IP-Adapter + AnimateDiff
**VRAM**: ~8.9 GB (56%)
**Input**:
- SCENE_PROMPT: Prompt de la escena
- POSE_IMAGE: Imagen de pose (de WF1)
- REFERENCE_IMAGE: Imagen de referencia (de WF2)

**Output**:
- Video MP4 guardado en: output/CoherentVideo/

**Tiempo**: 8-12 minutos por escena de 5 segundos

**Configuración optimizada**:
- batch_size: 1
- frames: 48
- fps: 8
- context_length: 16
- context_overlap: 4
- closed_loop: false

---

## 📋 FLUJO DE USO:

### Para cada escena:
1. **Abrir WF1** en ComfyUI
   - Configurar POSE_DESCRIPTION
   - Ejecutar
   - Guardar imagen de pose resultante

2. **Abrir WF2** en ComfyUI
   - Configurar CHARACTER_DESCRIPTION
   - Ejecutar
   - Guardar imagen de referencia

3. **Abrir WF3** en ComfyUI
   - Configurar SCENE_PROMPT
   - Cargar imagen de pose (WF1)
   - Cargar imagen de referencia (WF2)
   - Ejecutar
   - Obtener video de 5 segundos

4. **Repetir** para cada escena
5. **Ensamblar** videos con FFmpeg (script existente)

---

## ⚠️ NOTAS IMPORTANTES:

1. **NO ejecutar workflows en paralelo** (VRAM limitada)
2. **Cerrar workflow anterior** antes de abrir el siguiente
3. **Usar batch_size=1** siempre
4. **Modelos grandes en lowvram mode**
5. **Guardar outputs intermedios** para reutilizar

---

## 🔧 OPTIMIZACIONES APLICADAS:

- ControlNet OpenPose: nodos Advanced-ControlNet para compatibilidad sliding
- ControlNet strength recomendado para movimiento: 0.25-0.55
- IP-Adapter strength recomendado: 0.55-0.8 (según prioridad identidad vs acción)
- AnimateDiff context_length: 16 (óptimo para VRAM)
- Closed loop: false (narrativo no-loop)
- LoRA detail: 0.45 (calidad visual)
- LoRA noiseoffset: 0.3 (textura)

---

## 📊 ESPECIFICACIONES TÉCNICAS:

- Resolución: 768x432 (16:9 widescreen)
- Framerate: 8 fps (output)
- Duración por clip: 5 segundos (48 frames)
- Codec: H.264 MP4
- Modelo base: dreamshaper_8.safetensors

---

## 🎬 PRÓXIMO PASO:

Probar el sistema con una escena simple antes de producir el video completo.
