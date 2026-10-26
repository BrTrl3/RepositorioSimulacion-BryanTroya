import matplotlib.pyplot as plt


def _configurar_ejes(titulo):

    plt.xlabel("Tiempo")
    plt.ylabel("Poblacion")
    plt.title(titulo)
    plt.grid(True)
    plt.legend()


def graficar_modelos(
    t_deterministico,
    P_deterministico,
    t_discreto,
    P_discreto,
    t_estocastico,
    P_estocastico,
    t_continuo,
    P_continuo,
    datos=None
):

    plt.figure(figsize=(10, 5))

    plt.plot(
        t_deterministico,
        P_deterministico,
        label="Deterministico"
    )

    plt.plot(
        t_discreto,
        P_discreto,
        label="Discreto"
    )

    plt.plot(
        t_estocastico,
        P_estocastico,
        label="Estocastico"
    )

    plt.plot(
        t_continuo,
        P_continuo,
        label="Continuo - Euler"
    )

    if datos is not None:
        t_datos = list(range(len(datos)))
        plt.scatter(
            t_datos,
            datos,
            color="black",
            zorder=5,
            label="Datos de la guia"
        )

    _configurar_ejes(
        "Comparacion de modelos con los datos de la guia"
    )

    plt.tight_layout()
    plt.show()


def graficar_crecimiento_decrecimiento(
    t_det_crec,
    P_det_crec,
    t_dis_crec,
    P_dis_crec,
    t_con_crec,
    P_con_crec,
    t_det_dec,
    P_det_dec,
    t_dis_dec,
    P_dis_dec,
    t_con_dec,
    P_con_dec
):

    fig, (ax_crec, ax_dec) = plt.subplots(1, 2, figsize=(14, 5))

    ax_crec.plot(t_det_crec, P_det_crec, label="Deterministico")
    ax_crec.plot(t_dis_crec, P_dis_crec, label="Discreto")
    ax_crec.plot(t_con_crec, P_con_crec, label="Continuo - Euler")
    ax_crec.set_title("Crecimiento (r = 0.10)")
    ax_crec.set_xlabel("Tiempo")
    ax_crec.set_ylabel("Poblacion")
    ax_crec.grid(True)
    ax_crec.legend()

    ax_dec.plot(t_det_dec, P_det_dec, label="Deterministico")
    ax_dec.plot(t_dis_dec, P_dis_dec, label="Discreto")
    ax_dec.plot(t_con_dec, P_con_dec, label="Continuo - Euler")
    ax_dec.set_title("Decrecimiento (r = -0.05)")
    ax_dec.set_xlabel("Tiempo")
    ax_dec.set_ylabel("Poblacion")
    ax_dec.grid(True)
    ax_dec.legend()

    fig.suptitle("Escenarios de crecimiento y decrecimiento")
    fig.tight_layout()
    plt.show()


def graficar_influencia_r(curvas):

    plt.figure(figsize=(10, 5))

    for etiqueta, (t, P) in curvas.items():
        plt.plot(t, P, label=etiqueta)

    _configurar_ejes("Influencia de la tasa de crecimiento r")

    plt.tight_layout()
    plt.show()


def graficar_replicas_estocasticas(
    t,
    replicas,
    promedio,
    t_deterministico,
    P_deterministico
):

    plt.figure(figsize=(10, 5))

    for i, P in enumerate(replicas):
        plt.plot(
            t,
            P,
            color="tab:orange",
            alpha=0.25,
            label="Replicas estocasticas" if i == 0 else None
        )

    plt.plot(
        t,
        promedio,
        color="tab:red",
        linewidth=2,
        label="Promedio estocastico"
    )

    plt.plot(
        t_deterministico,
        P_deterministico,
        color="tab:blue",
        linewidth=2,
        label="Deterministico"
    )

    _configurar_ejes("Efecto de la aleatoriedad (30 replicas)")

    plt.tight_layout()
    plt.show()
