#version 3.7

global_settings {
    assumed_gamma 1.0
}

#declare OvalLargura = 0.95;
#declare OvalAltura  = 1.55;
#declare OvalProf    = 0.18;

#declare LuaLargura = 0.82;
#declare LuaAltura  = 1.18;
#declare LuaOffX    = 0.55;
#declare LuaOffY    = 0.25;

#declare CirRaio = 0.42;
#declare CirX    = 0.38;
#declare CirY    = 0.45;

#declare FaixaEsp  = 0.055;
#declare FaixaLarg = 3.00;

#declare FaixaSup1Y = 0.56;
#declare FaixaSup2Y = 0.40;

#declare FaixaInf1Y = -0.88;
#declare FaixaInf2Y = -1.08;

#declare AzulUNIJUI = rgb <0.0, 0.2706, 0.5569>;

#declare TexturaAzul =
texture {
    pigment {
        color AzulUNIJUI
    }
    finish {
        ambient 0.15
        diffuse 0.75
        specular 0.25
        roughness 0.05
    }
}

camera {
    orthographic
    location <0,0,10>
    look_at <0,0,0>
    right x*2.2
    up y*3.2
}

light_source {
    <-3,4,8>
    color rgb <1,1,1>
    shadowless
}

light_source {
    <4,-2,6>
    color rgb <0.35,0.35,0.40>
    shadowless
}

background {
    color rgb <1,1,1>
}

#macro OvalDisco(cx,cy,sx,sy,sz)
    sphere {
        <0,0,0>, 1
        scale <sx,sy,sz>
        translate <cx,cy,0>
    }
#end

#macro FaixaBox(cx,cy,esp)
    box {
        <-FaixaLarg/2,-esp/2,-1>,
        < FaixaLarg/2, esp/2, 1>
        translate <cx,cy,0>
    }
#end

union {

    difference {

        difference {

            OvalDisco(
                0,0,
                OvalLargura,
                OvalAltura,
                OvalProf
            )

            OvalDisco(
                LuaOffX,
                LuaOffY,
                LuaLargura,
                LuaAltura,
                OvalProf*3
            )
        }

        FaixaBox(0,FaixaInf1Y,FaixaEsp)
        FaixaBox(0,FaixaInf2Y,FaixaEsp)
    }

    difference {

        OvalDisco(
            CirX,
            CirY,
            CirRaio,
            CirRaio,
            OvalProf
        )

        FaixaBox(0,FaixaSup1Y,FaixaEsp)
        FaixaBox(0,FaixaSup2Y,FaixaEsp)
    }

    intersection {
        OvalDisco(
            0,0,
            OvalLargura,
            OvalAltura,
            OvalProf*2
        )

        FaixaBox(
            0,
            FaixaInf1Y - FaixaEsp,
            FaixaEsp
        )
    }

    intersection {
        OvalDisco(
            0,0,
            OvalLargura,
            OvalAltura,
            OvalProf*2
        )

        FaixaBox(
            0,
            (FaixaInf1Y + FaixaInf2Y)/2,
            FaixaEsp
        )
    }

    intersection {
        OvalDisco(
            0,0,
            OvalLargura,
            OvalAltura,
            OvalProf*2
        )

        FaixaBox(
            0,
            FaixaInf2Y + FaixaEsp,
            FaixaEsp
        )
    }

    texture {
        TexturaAzul
    }

    scale <-1,1,1>
}