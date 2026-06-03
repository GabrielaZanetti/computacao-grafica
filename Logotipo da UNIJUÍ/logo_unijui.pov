// ============================================================
// Aula 12 - Reprodução do Logotipo da UNIJUÍ
// Modelagem CSG no POV-Ray
//
// Acadêmico: [SEU NOME COMPLETO AQUI]
// Disciplina: Computação Gráfica
// Data: 2025
//
// DESCRIÇÃO DO LOGOTIPO:
//   (a) Oval vertical externa (corpo principal azul)
//   (b) Recorte de lua crescente no canto superior direito
//       (diferença entre dois ovais)
//   (c) Círculo interno no canto superior direito
//   (d) Quatro faixas horizontais:
//       - Duas cortando o círculo interno (topo)
//       - Duas cortando a base da oval externa (base)
//   (e) Cor azul institucional #0E3D8C
// ============================================================

#version 3.7;
global_settings { assumed_gamma 1.0 }

// ============================================================
// PARÂMETROS GLOBAIS (fácil ajuste de proporções)
// ============================================================

// --- Oval externa ---
#declare OvalLargura  = 1.10;   // escala X da oval externa
#declare OvalAltura   = 1.40;   // escala Y da oval externa
#declare OvalProf     = 0.18;   // espessura (profundidade Z)

// --- Lua crescente: oval de recorte ---
#declare LuaLargura   = 0.90;   // escala X do oval de corte
#declare LuaAltura    = 0.90;   // escala Y do oval de corte
#declare LuaOffX      = 0.75;   // deslocamento X do oval de corte (para direita)
#declare LuaOffY      = 0.55;   // deslocamento Y do oval de corte (para cima)

// --- Círculo interno ---
#declare CirRaio      = 0.46;   // raio do círculo interno
#declare CirX         = 0.42;   // posição X do círculo
#declare CirY         = 0.52;   // posição Y do círculo

// --- Faixas horizontais (espessura e posições) ---
#declare FaixaEsp     = 0.062;  // espessura de cada faixa
#declare FaixaLarg    = 2.50;   // largura das faixas (maior que o logo)

// Faixas superiores (cortam o círculo interno)
#declare FaixaSup1Y   =  0.40;  // posição Y da faixa superior 1
#declare FaixaSup2Y   =  0.24;  // posição Y da faixa superior 2

// Faixas inferiores (cortam a base da oval)
#declare FaixaInf1Y   = -0.88;  // posição Y da faixa inferior 1
#declare FaixaInf2Y   = -1.04;  // posição Y da faixa inferior 2

// --- Cor azul institucional UNIJUÍ ---
#declare AzulUNIJUI = rgb <0.055, 0.239, 0.549>;
// Versão ligeiramente mais clara para destaque
#declare AzulClaro  = rgb <0.07,  0.30,  0.65>;

// ============================================================
// TEXTURA / MATERIAL
// ============================================================

// Textura principal azul com leve brilho
#declare TexturaAzul = texture {
    pigment { color AzulUNIJUI }
    finish {
        ambient    0.15
        diffuse    0.75
        specular   0.35
        roughness  0.05
        reflection 0.05
    }
}

// ============================================================
// CÂMERA
// ============================================================
// Visão frontal, centralizada no logotipo
camera {
    orthographic
    location  <0, 0, 10>
    look_at   <0, 0, 0>
    right     x * 3.2
    up        y * 3.8
}

// ============================================================
// ILUMINAÇÃO
// ============================================================

// Luz principal — frontal levemente à esquerda e acima
light_source {
    <-3, 4, 8>
    color rgb <1.0, 1.0, 1.0>
    shadowless
}

// Luz de preenchimento — suave, lado direito
light_source {
    <4, -2, 6>
    color rgb <0.35, 0.35, 0.40>
    shadowless
}

// ============================================================
// FUNDO
// ============================================================
background { color rgb <1, 1, 1> }  // fundo branco

// ============================================================
// MACROS AUXILIARES
// ============================================================

// Macro: gera um "disco oval" (esfera achatada via scale)
// cx, cy = centro;  sx = escala X;  sy = escala Y;  sz = profundidade Z
#macro OvalDisco(cx, cy, sx, sy, sz)
    sphere {
        <0, 0, 0>, 1
        scale <sx, sy, sz>
        translate <cx, cy, 0>
    }
#end

// Macro: caixa horizontal (faixa) centrada em (cx, cy)
#macro FaixaBox(cx, cy, espessura)
    box {
        <-FaixaLarg/2, -espessura/2, -OvalProf*2>,
        < FaixaLarg/2,  espessura/2,  OvalProf*2>
        translate <cx, cy, 0>
    }
#end

// ============================================================
// CONSTRUÇÃO DO LOGOTIPO
// ============================================================

// -----------------------------------------------------------
// OBJETO PRINCIPAL: union de todas as partes azuis
// -----------------------------------------------------------
union {

    // -------------------------------------------------------
    // PARTE 1 — Oval externa com lua crescente recortada
    // (difference: oval_externa - oval_recorte)
    // -------------------------------------------------------
    difference {
        // Oval externa (corpo principal)
        OvalDisco(0, 0, OvalLargura, OvalAltura, OvalProf)

        // Oval de recorte (cria o efeito de lua crescente)
        OvalDisco(LuaOffX, LuaOffY, LuaLargura, LuaAltura, OvalProf*3)
    }

    // -------------------------------------------------------
    // PARTE 2 — Círculo interno (sem as faixas = difference)
    // O círculo aparece dentro do recorte da lua
    // -------------------------------------------------------
    difference {
        // Círculo (esfera achatada = disco)
        OvalDisco(CirX, CirY, CirRaio, CirRaio, OvalProf)

        // Subtrai as duas faixas horizontais superiores
        // para criar o efeito de listras no círculo
        FaixaBox(0, FaixaSup1Y, FaixaEsp)
        FaixaBox(0, FaixaSup2Y, FaixaEsp)
    }

    // -------------------------------------------------------
    // PARTE 3 — Faixas horizontais INFERIORES
    // Cortam a oval externa na região da base
    // (intersection: faixa ∩ oval_externa)
    // -------------------------------------------------------

    // Faixa inferior 1
    intersection {
        OvalDisco(0, 0, OvalLargura, OvalAltura, OvalProf*2)
        FaixaBox(0, FaixaInf1Y, FaixaEsp)
    }

    // Faixa inferior 2
    intersection {
        OvalDisco(0, 0, OvalLargura, OvalAltura, OvalProf*2)
        FaixaBox(0, FaixaInf2Y, FaixaEsp)
    }

    // -------------------------------------------------------
    // Aplica textura azul a todo o conjunto
    // -------------------------------------------------------
    texture { TexturaAzul }

} // fim union principal

// ============================================================
// FIM DO ARQUIVO
// ============================================================
