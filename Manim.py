import json
from manim import *

class BSTAnimation(Scene):
    def construct(self):
        # Título principal
        title = Text("Operaciones BST: Inserción, Búsqueda y Eliminación", font_size=30)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Coordenadas estáticas para posicionar los nodos (incluye los nodos 14 y 4)
        # Coordenadas estáticas para posicionar los nodos (incluye 14, 4 y 9)
        layout = {
            8: [0, 2.2, 0],
            3: [-2.5, 0.8, 0],
            10: [2.5, 0.8, 0],
            1: [-3.8, -0.6, 0],
            6: [-1.2, -0.6, 0],
            9: [1.2, -0.6, 0],
            14: [3.8, -0.6, 0],
            4: [-2.0, -2.0, 0]
        }

        try:
            with open("trace.json", "r") as f:
                trace = json.load(f)
        except FileNotFoundError:
            trace = []

        graph = None

        def build_node(val, color=BLUE):
            circle = Circle(radius=0.35, fill_color=color, fill_opacity=1, stroke_color=WHITE)
            label = Text(str(val), font_size=20, color=WHITE)
            return VGroup(circle, label)

        for step in trace:
            action = step.get("action")
            val = step.get("value")
            path = step.get("path", [])

            # --- INSERCIÓN ---
            if action == "insert":
                header = Text(f"Insertando nodo: {val}", font_size=28, color=YELLOW).to_edge(UP)
                self.play(Write(header))
                self.wait(0.3)

                if graph is not None and path:
                    moving_node = build_node(val, color=ORANGE)
                    moving_node.move_to([-5, 2, 0])
                    self.play(FadeIn(moving_node))

                    for parent_val in path:
                        parent_pos = layout[parent_val]
                        self.play(moving_node.animate.move_to(parent_pos), run_time=0.7)

                        if val < parent_val:
                            cmp_text = f"{val} < {parent_val} → Ir a la Izquierda"
                        else:
                            cmp_text = f"{val} > {parent_val} → Ir a la Derecha"

                        cmp_banner = Text(cmp_text, font_size=20, color=BLUE_A).next_to(header, DOWN)
                        self.play(Write(cmp_banner), run_time=0.4)
                        self.wait(0.6)
                        self.play(FadeOut(cmp_banner), run_time=0.3)

                    empty_text = Text(f"¡Posición libre encontrada para {val}!", font_size=20, color=GREEN).next_to(header, DOWN)
                    self.play(Write(empty_text), run_time=0.4)
                    self.wait(0.5)
                    self.play(FadeOut(empty_text), FadeOut(moving_node), run_time=0.3)

                if graph is None:
                    node_mob = build_node(val)
                    graph = Graph(
                        [val],
                        [],
                        layout={val: layout[val]},
                        vertex_mobjects={val: node_mob}
                    )
                    self.play(Create(graph))
                else:
                    new_edge = (path[-1], val)
                    new_node_mob = build_node(val)

                    self.play(
                        graph.animate.add_vertices(
                            val,
                            positions={val: layout[val]},
                            vertex_mobjects={val: new_node_mob}
                        )
                    )
                    self.play(
                        graph.animate.add_edges(new_edge)
                    )

                self.play(FadeOut(header))
                self.wait(0.5)

            # --- BÚSQUEDA ---
            elif action == "search":
                is_found = step.get("found", False)
                header = Text(f"Buscando nodo: {val}", font_size=28, color=TEAL).to_edge(UP)
                self.play(Write(header))
                self.wait(0.3)

                if graph is not None and path:
                    moving_node = build_node(val, color=PURPLE)
                    moving_node.move_to([-5, 2, 0])
                    self.play(FadeIn(moving_node))

                    for current_node in path:
                        pos = layout[current_node]
                        self.play(moving_node.animate.move_to(pos), run_time=0.7)

                        if val == current_node:
                            cmp_text = f"¡{val} == {current_node}! Elemento encontrado"
                            cmp_banner = Text(cmp_text, font_size=20, color=GREEN).next_to(header, DOWN)
                            self.play(Write(cmp_banner), run_time=0.4)
                            self.wait(0.8)
                            self.play(FadeOut(cmp_banner), run_time=0.3)
                        else:
                            if val < current_node:
                                cmp_text = f"{val} < {current_node} → Ir a la Izquierda"
                            else:
                                cmp_text = f"{val} > {current_node} → Ir a la Derecha"

                            cmp_banner = Text(cmp_text, font_size=20, color=BLUE_A).next_to(header, DOWN)
                            self.play(Write(cmp_banner), run_time=0.4)
                            self.wait(0.6)
                            self.play(FadeOut(cmp_banner), run_time=0.3)

                    self.play(FadeOut(moving_node))

                if not is_found:
                    empty_text = Text(f"Nodo siguiente vacío → El nodo {val} NO existe", font_size=20, color=RED).next_to(header, DOWN)
                    self.play(Write(empty_text), run_time=0.5)
                    self.wait(1.0)
                    self.play(FadeOut(empty_text))

                txt_color = GREEN if is_found else RED
                result_msg = f"Resultado: {'¡Nodo ' + str(val) + ' Encontrado!' if is_found else 'Nodo ' + str(val) + ' No existe'}"
                banner = Text(result_msg, color=txt_color, font_size=24).next_to(header, DOWN)
                self.play(Write(banner))
                self.wait(1.2)
                self.play(FadeOut(banner), FadeOut(header))

            # --- ELIMINACIÓN ---
            elif action == "delete":
                is_found = step.get("found", False)
                header = Text(f"Eliminando nodo: {val}", font_size=28, color=RED_B).to_edge(UP)
                self.play(Write(header))
                self.wait(0.3)

                if graph is not None and path:
                    moving_node = build_node(val, color=RED_A)
                    moving_node.move_to([-5, 2, 0])
                    self.play(FadeIn(moving_node))

                    for current_node in path:
                        pos = layout[current_node]
                        self.play(moving_node.animate.move_to(pos), run_time=0.7)

                        if val == current_node:
                            cmp_text = f"¡Nodo {val} ubicado para eliminación!"
                            cmp_banner = Text(cmp_text, font_size=20, color=RED).next_to(header, DOWN)
                            self.play(Write(cmp_banner), run_time=0.4)
                            self.wait(0.8)
                            self.play(FadeOut(cmp_banner), run_time=0.3)
                        else:
                            if val < current_node:
                                cmp_text = f"{val} < {current_node} → Ir a la Izquierda"
                            else:
                                cmp_text = f"{val} > {current_node} → Ir a la Derecha"

                            cmp_banner = Text(cmp_text, font_size=20, color=BLUE_A).next_to(header, DOWN)
                            self.play(Write(cmp_banner), run_time=0.4)
                            self.wait(0.6)
                            self.play(FadeOut(cmp_banner), run_time=0.3)

                    self.play(FadeOut(moving_node))

                if is_found:
                    # Si tiene padre, remover la arista primero
                    if len(path) > 1:
                        parent_val = path[-2]
                        # Identificar el par de la arista en orden correcto
                        edge_to_remove = (parent_val, val) if (parent_val, val) in graph.edges else (val, parent_val)
                        self.play(graph.animate.remove_edges(edge_to_remove))

                    # Remover el vértice del grafo
                    self.play(graph.animate.remove_vertices(val))

                    confirm_msg = Text(f"Nodo {val} eliminado con éxito", font_size=20, color=GREEN).next_to(header, DOWN)
                    self.play(Write(confirm_msg))
                    self.wait(1.0)
                    self.play(FadeOut(confirm_msg))
                else:
                    empty_text = Text(f"Nodo siguiente vacío → No se puede eliminar {val} (No existe)", font_size=20, color=RED).next_to(header, DOWN)
                    self.play(Write(empty_text), run_time=0.5)
                    self.wait(1.2)
                    self.play(FadeOut(empty_text))

                self.play(FadeOut(header))
                self.wait(0.5)

            # --- RECORRIDOS (INORDER, PREORDER, POSTORDER) ---
            elif action in ["inorder", "preorder", "postorder"]:
                titles = {
                    "inorder": "Recorrido Inorden",
                    "preorder": "Recorrido Preorden",
                    "postorder": "Recorrido Postorden"
                }

                header = Text(titles[action], font_size=28, color=YELLOW).to_edge(UP)
                self.play(Write(header))

                sequence = []
                bottom_list_mob = None

                for item in path:
                    # Resaltar en amarillo el nodo visitado
                    highlight = Circle(radius=0.4, color=YELLOW, stroke_width=4).move_to(layout[item])
                    self.play(Create(highlight), run_time=0.4)

                    sequence.append(str(item))
                    formatted_seq = " -> ".join(sequence)

                    new_bottom = Text(f"Orden: [ {formatted_seq} ]", font_size=22, color=BLUE_A).to_edge(DOWN)

                    if bottom_list_mob is None:
                        self.play(Write(new_bottom), run_time=0.5)
                        bottom_list_mob = new_bottom
                    else:
                        self.play(Transform(bottom_list_mob, new_bottom), run_time=0.5)

                    self.wait(0.4)
                    self.play(Uncreate(highlight), run_time=0.3)

                # Cartel de finalización al terminar la secuencia completa
                status_msg = Text("¡Terminado!", font_size=24, color=GREEN).next_to(bottom_list_mob, UP)
                self.play(Write(status_msg))
                self.wait(2)

                self.play(
                    FadeOut(header),
                    FadeOut(status_msg),
                    FadeOut(bottom_list_mob)
                )
                self.wait(0.5)

        self.wait(2)