--
-- PostgreSQL database dump
--

\restrict RHf9qM2Ft4QygYp0lxzZ7CBqLW4aRavKpD16q8dw8GGlpCd396PGuThQM3coJfa

-- Dumped from database version 18.4 (Ubuntu 18.4-0ubuntu0.26.04.1)
-- Dumped by pg_dump version 18.4 (Ubuntu 18.4-0ubuntu0.26.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: cart_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cart_items (
    id integer NOT NULL,
    cart_id integer NOT NULL,
    produto_id integer NOT NULL,
    quantidade integer
);


ALTER TABLE public.cart_items OWNER TO postgres;

--
-- Name: cart_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cart_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cart_items_id_seq OWNER TO postgres;

--
-- Name: cart_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cart_items_id_seq OWNED BY public.cart_items.id;


--
-- Name: carts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.carts (
    id integer NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.carts OWNER TO postgres;

--
-- Name: carts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.carts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.carts_id_seq OWNER TO postgres;

--
-- Name: carts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.carts_id_seq OWNED BY public.carts.id;


--
-- Name: categorias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categorias (
    id integer NOT NULL,
    nome character varying(100) NOT NULL,
    slug character varying(100) NOT NULL,
    descricao text,
    ativo boolean
);


ALTER TABLE public.categorias OWNER TO postgres;

--
-- Name: categorias_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categorias_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categorias_id_seq OWNER TO postgres;

--
-- Name: categorias_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categorias_id_seq OWNED BY public.categorias.id;


--
-- Name: produtos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.produtos (
    id integer NOT NULL,
    slug character varying(100) NOT NULL,
    nome character varying(150) NOT NULL,
    preco double precision NOT NULL,
    imagem character varying(255) NOT NULL,
    descricao text,
    categoria character varying(100),
    preco_antigo double precision,
    desconto integer,
    promocao boolean,
    destaque boolean,
    ativo boolean,
    stock integer,
    criado_em timestamp without time zone,
    atualizado_em timestamp without time zone
);


ALTER TABLE public.produtos OWNER TO postgres;

--
-- Name: produtos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.produtos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.produtos_id_seq OWNER TO postgres;

--
-- Name: produtos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.produtos_id_seq OWNED BY public.produtos.id;


--
-- Name: rating; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rating (
    id integer NOT NULL,
    valor integer NOT NULL,
    user_id integer,
    produto_id integer
);


ALTER TABLE public.rating OWNER TO postgres;

--
-- Name: rating_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rating_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rating_id_seq OWNER TO postgres;

--
-- Name: rating_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rating_id_seq OWNED BY public.rating.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(255) NOT NULL,
    phone character varying(20) NOT NULL,
    reset_code character varying(6),
    reset_code_expires timestamp without time zone,
    is_admin boolean
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: cart_items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items ALTER COLUMN id SET DEFAULT nextval('public.cart_items_id_seq'::regclass);


--
-- Name: carts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carts ALTER COLUMN id SET DEFAULT nextval('public.carts_id_seq'::regclass);


--
-- Name: categorias id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias ALTER COLUMN id SET DEFAULT nextval('public.categorias_id_seq'::regclass);


--
-- Name: produtos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produtos ALTER COLUMN id SET DEFAULT nextval('public.produtos_id_seq'::regclass);


--
-- Name: rating id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rating ALTER COLUMN id SET DEFAULT nextval('public.rating_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
4e8ac0c8a66e
\.


--
-- Data for Name: cart_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cart_items (id, cart_id, produto_id, quantidade) FROM stdin;
\.


--
-- Data for Name: carts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.carts (id, user_id, created_at) FROM stdin;
3	3	2026-07-01 13:03:03.882198
4	4	2026-07-02 07:08:33.723972
\.


--
-- Data for Name: categorias; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categorias (id, nome, slug, descricao, ativo) FROM stdin;
\.


--
-- Data for Name: produtos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.produtos (id, slug, nome, preco, imagem, descricao, categoria, preco_antigo, desconto, promocao, destaque, ativo, stock, criado_em, atualizado_em) FROM stdin;
1	anabolic_muscle_4kg	HUGE Anabolic Muscle 4KG	2100	img/anabolicmuscle_4kg-removebg-preview.png	<p>É um suplemento do tipo hipercalórico (mass gainer), indicado para quem quer ganhar peso e massa muscular. <br/>  Principais Benefícios:</p>\n                            <ol>\n                                <li>Ajuda no ganho de massa muscular;</li>\n                                <li>Aumenta ingestão calórica diária;</li>\n                                <li>Auxilia na recuperação pós-treino;</li>\n                                <li>Pode melhorar força e desempenho.</li>\n                            </ol> \n<h4>Composição típica</h4>\n                                <ol>\n                                    Uma dose costuma ter cerca de:\n                                    <li>Proteína (≈40–50g por dose)  - Mistura de whey protein, proteína de soja e outras fontes — ajuda na construção e reparação muscular;</li>\n                                    <li>Carboidratos (≈60–90g por dose) - Geralmente maltodextrina e dextrose — fornecem energia e ajudam a repor o glicogênio muscular;</li>\n                                    <li>Creatina (≈3–5g) - Pode ajudar no aumento de força e desempenho em exercícios intensos;</li>\n                                    <li>Aminoácidos e vitaminas - Apoiam recuperação muscular e metabolismo energético;</li>\n                                    <li>Calorias elevadas - Ideal para quem precisa aumentar a ingestão calórica diária.</li>\n                                </ol>\n<h4>Como é usado</h4>\n                                <p>Uso comum recomendado pelo fabricante:</p>\n                                <ol>\n                                    <li>Misturar 3–4 colheres (aprox. 150g);</li>\n                                    <li>Adicionar 500–600ml de água ou leite;</li>\n                                    <li>Agitar bem até dissolver;</li>\n                                    <li>Consumir 1–2 vezes ao dia.</li>\n                                </ol>\n                                <p><strong>Melhor momento:</strong></p>\n                                <ol>\n                                    <li>Após o treino;</li>\n                                    <li>Ou entre refeições para aumentar calorias.</li>\n                                </ol>\n<h4>Importante saber</h4>\n                                <ol>\n                                    <li>Este tipo de suplemento não substitui uma dieta equilibrada e não faz “milagres”. O ganho de peso/massa depende da sua alimentação e do treino.</li>\n                                    <li>Muitos fabricantes recomendam consultar um profissional de saúde antes de usar, especialmente se você tiver alguma condição médica, for menor de 18 anos ou estiver grávida/nutrindo bebê.</li>\n                                    <li>Suplementos e outros produtos importados podem variar em preço e sabor dependendo do país e fornecedor.</li>\n                                </ol>	hipercalorico	\N	\N	\N	\N	\N	\N	\N	\N
2	fast_grow_4kg	USN FAST GROW ANABOLIC GH 4KG	3750	img/fastgrow_4kg-removebg-preview.png	<p>É um suplemento alimentar em pó projetado principalmente para pessoas que querem:</p>\n                        <ol>\n                            <li>Ajudar no crescimento muscular;</li>\n                            <li>Suportar recuperação após treinos;</li>\n                            <li>Fornecer proteína e calorias extras para quem tem dificuldade em ganhar peso.</li>\n                        </ol>\n                        <p>\n                            Ele combina fontes de proteína, carboidratos e outros ingredientes numa fórmula “all-in-one” — ou seja, vários nutrientes num mesmo produto\n                        </p>\n<h4>Composição típica (por dose ~150 g)</h4>\n                            <ol>\n                                <li>~50–55 g de proteína (mistura de whey, caseína e proteína de soja) — ajuda a reparar fibras musculares.</li>\n                                <li>Carboidratos (maltodextrina, dextrose) — para dar energia e ajudar a repor glicogênio.</li>\n                                <li>Creatina (≈5000 mg) — pode ajudar no desempenho de exercícios de alta intensidade.</li>\n                                <li>Aminoácidos, taurina e tribulus — ingredientes que algumas marcas usam para apoiar a síntese de proteína e força, embora evidência forte possa ser variável.</li>\n                            </ol>\n<h4>Como é usado</h4>\n                            <p>  Geralmente, a recomendação do fabricante é:</p>\n                            <ol>\n                                <li>~Misturar 3 colheres (~150 g) em cerca de 600-650 ml de água;</li>\n                                <li>Tomar 1-2 vezes por dia, entre refeições ou conforme o plano de nutrição;</li>\n                                <li>Pessoas com peso maior podem iniciar com mais porções nos primeiros dias e depois ajustar conforme necessário.</li>\n                            </ol>\n<h4>Importante saber</h4>\n                            <ol>\n                                <li>Este tipo de suplemento não substitui uma dieta equilibrada e não faz “milagres”. O ganho de peso/massa depende da sua alimentação e do treino.</li>\n                                <li>Muitos fabricantes recomendam consultar um profissional de saúde antes de usar, especialmente se você tiver alguma condição médica, for menor de 18 anos ou estiver grávida/nutrindo bebê.</li>\n                                <li>Suplementos e outros produtos importados podem variar em preço e sabor dependendo do país e fornecedor.</li>\n                            </ol>	hipercalorico	\N	\N	\N	\N	\N	\N	\N	\N
3	hyperbolic_mass_4kg	USN HYPERBOLIC MASS GH 4KG	2500	img/hyperbolic_4kg-removebg-preview.png	<p>É um suplemento alimentar do tipo hipercalórico (mass gainer), normalmente utilizado por quem tem dificuldade em ganhar peso ou quer aumentar a ingestão calórica para crescimento muscular.<br/> Serve para:</p>\n                        <ol>\n                            <li>Aumentar o consumo de calorias diárias;</li>\n                            <li>Auxiliar no ganho de massa muscular;</li>\n                            <li>Melhorar a recuperação pós-treino;</li>\n                        </ol>\n<p>Composição típica (pode variar um pouco, mas geralmente contém:)</p>\n                            <ol>\n                                <li>Carboidratos (60–75%) - Principal fonte de energia;</li>\n                                <li>Proteína (10–25%) - Pode vir do soro do leite (whey);</li>\n                                <li>Gorduras (baixa a moderada quantidade) - Auxiliam no aporte calórico;</li>\n                                <li>Vitaminas e Minerais - Complexo B, Ferro, Zinco, Cálcio</li>\n                            </ol>\n<h4>Como é usado</h4>\n                            <ol>\n                              \n                                <li>Misturar 1 dose (conforme a embalagem) com 250–500 ml de água ou leite;</li>\n                                <li>Tomar após o treino (mais comum) ou entre refeições;</li>\n                                <li>Pessoas com peso maior podem iniciar com menos porções nos primeiros dias e depois ajustar conforme necessário.</li>\n                            </ol>\n<h4>Importante saber</h4>\n                            <ol>\n                                <li>Não substitui alimentação sólida;</li>\n                                <li>Pode causar aumento de gordura se usado em excesso;</li>\n                                <li>Ideal para quem tem dificuldade real em ganhar peso;</li>\n                                <li>Deve ser combinado com treino de musculação.</li>\n                            </ol>	hipercalorico	\N	\N	\N	\N	\N	\N	\N	\N
4	hyper_gain_mass_4kg	NPL HYPER GAIN MASS 4KG	2300	img/hypergainer_4kg-removebg-preview.png	<p>É um suplemento hipercalórico (mass gainer), e o principal objetivo dele é ajudar pessoas a ganhar peso e massa muscular de forma mais rápida e prática.<br/> Serve para:</p>\n<h4>Como é usado</h4>\n                                <ol>\n                                \n                                    <li>Misture com água ou leite (250–600 ml) para fazer o shake;</li>\n                                    <li>Porções diárias: 1 a 3 shakes por dia, dependendo da necessidade calórica e volume de treino;</li>\n                                    <li>Quando tomar: após o treino, entre as refeições, como complemento de calorias quando for difícil comer mais comida sólida</li>\n                                </ol>\n<h4>Importante saber</h4>\n                                <ol>\n                                    <li>É um suplemento, não um alimento principal – você ainda precisa comer bem;</li>\n                                    <li>Pode ajudar a ganhar peso, mas se fizer muito além do que precisas, pode ganhar gordura;</li>\n                                    <li>Hidratação e treino consistente são essenciais para resultados;</li>\n                                    <li>Muitos profissionais recomendam consultar um nutricionista antes de usar.</li>\n                                </ol>\n                            <ol>\n                                <li>Aumentar a ingestão calórica;</li>\n                                <li>Auxiliar no ganho de massa muscular;</li>\n                                <li>Melhorar a recuperação pós-treino;</li>\n                                <li>Ajudar pessoas com metabolismo acelerado.</li>\n                            </ol>\n<p>Embora a tabela exata dependendo da marca e sabor, produtos como esse costumam incluir:</p>\n                                <ol>\n                                    <li>Carboidratos (60–75%) - Principal fonte de energia;</li>\n                                    <li>Proteína (10–25%) - ajuda na construção muscular;</li>\n                                    <li>Gorduras - geralmente em menor quantidade (a quantidade exata depende da versão e sabor);</li>\n                                    <li>Vitaminas e Minerais - para apoiar o metabolismo geral;</li>\n                                    <li>L‑Glutamina e Tribulus (em algumas versões) — para recuperação e suporte muscular</li>\n                                    <li>Creatina — pode ajudar no desempenho de força.</li>\n                                </ol>	hipercalorico	\N	\N	\N	\N	\N	\N	\N	\N
5	hulk_gainer_4kg	NUTRITECH HULK GAINER ANABOLIC 4KG	2100	img/hulkgainer_4kg-removebg-preview.png	<p>É um suplementos chamado mass gainer (hipercalórico), feito para ajudar no ganho de peso e massa muscular quando usado com treino e alimentação apropriada.<br/> Serve para:</p>\n                            <ol>\n                                <li>Aumentar a ingestão calórica;</li>\n                                <li>Auxiliar no ganho de massa muscular;</li>\n                                <li>Melhorar a recuperação pós-treino;</li>\n                                <li>Ajudar pessoas com metabolismo acelerado.</li>\n                            </ol>\n<p>Embora a tabela exata dependendo da marca e sabor, produtos como esse costumam incluir:</p>\n                                <ol>\n                                    <li>Carboidratos (~165 g) — fornecem energia e ajudam a ganhar peso;</li>\n                                    <li>Proteínas (~30 g) — pra ajudar a construir músculo;</li>\n                                    <li>Vitaminas e Minerais - para apoiar o metabolismo geral;</li>\n                                    <li>Creatina (~5 g) — pode melhorar força e recuperação em algumas fórmulas.</li>\n                                </ol>\n<h4>Como é usado</h4>\n                                <ol>\n                                    <li>Misture 3 scoops com água ou leite para um shake calórico grande.</li>\n                                    <li>Pode tomar 1–3 vezes por dia dependendo de quantas calorias extras precisas;</li>\n                                    <li>Muitas pessoas tomam após o treino, ou entre refeições quando estão com dificuldade de comer o suficiente.</li>\n                                </ol>\n<h4>Importante saber</h4>\n                                <ol>\n                                    <li>Não substitui refeições completas — é um suplemento para complementar a dieta;</li>\n                                    <li>Se usado sem treino adequado pode levar a ganho de gordura, não só músculo;</li>\n                                    <li>É melhor combinar com uma alimentação equilibrada e um plano de treino;</li>\n                                    <li>Não é recomendado para menores de 18 anos sem orientação de um profissional de saúde.</li>\n                                </ol>	hipercalorico	\N	\N	\N	\N	\N	\N	\N	\N
6	usn_creatine_pure_200g	USN CREATINE PURE 200G	900	img/creatineusn_200gr-removebg-preview.png	<p>É um suplemento de creatina monohidratada micronizada pura, usado para melhorar desempenho, força e recuperação em treinos intensos.<br/> Principais Benefícios:</p>\n                            <ol>\n                                <li>Aumenta a energia disponível nos músculos para exercícios curtos e intensos, como séries de musculação;</li>\n                                <li>Melhora a força e potência muscular;</li>\n                                <li>Pode acelerar a recuperação entre séries e treinos;</li>\n                                <li>Facilita a síntese proteica quando combinada com treino e alimentos ricos em proteína.</li>\n                            </ol>\n<h4>Como é usado</h4>\n                                <p>Uso diário normal (mais comum):</p>\n                                <ol>\n                                    <li>3 a 5 gramas por dia;</li>\n                                    <li>Misturar em 200–250 ml de água;</li>\n                                    <li>Tomar 1 vez ao dia;</li>\n                                </ol>\n                                <p><strong>Melhor momento:</strong></p>\n                                <ol>\n                                    <li>Após o treino;</li>\n                                    <li>Ou entre refeições para aumentar calorias.</li>\n                                </ol>\n<h4>Fase de carga (opcional)</h4>\n                                <p>\n                                    Algumas pessoas fazem:\n                                </p>\n                                <ol>\n                                    <li>20 g por dia (dividido em 4 doses de 5 g) por 5–7 dias;</li>\n                                </ol>\n                                <p>\n                                    Depois:\n                                </p>\n                                <ol>\n                                    <li>\n                                        3–5 g por dia para manutenção;\n                                    </li>\n                                </ol>\n<h4>Importante saber</h4>\n                                <ol>\n                                    <li>Beba bastante água durante o dia.</li>\n                                    <li>Não precisa misturar com açúcar obrigatoriamente.</li>\n                                    <li>Pode tomar junto com whey protein.</li>\n                                    <li>Não precisa fazer “ciclos” obrigatoriamente.</li>\n                                </ol>	creatina	\N	\N	\N	\N	\N	\N	\N	\N
7	usn_creatine_3-in-1_200g	USN CREATINE 3-IN-1 200G	900	img/creatine3in1_200gr-removebg-preview.png	<p>É um suplemento à base de creatina combinado com outros ingredientes projetado para melhorar força, desempenho e recuperação muscular durante treinos intensos.Ele costuma combinar:</p>\n                        <ol>\n                            <li>Creatina monohidratada (forma mais estudada e eficaz);</li>\n                            <li>Beta-alanina – pode ajudar na resistência muscular;</li>\n                            <li>BCAAs ou outros aminoácidos – cozinham recuperação e síntese proteica.</li>\n                        </ol>\n<h4>Principais efeitos esperados</h4>\n                            <ol>\n                                <li>Aumento de força e potência;</li>\n                                <li>Mais resistência muscular;</li>\n                                <li>Recuperação mais rápida;</li>\n                                <li>Suporte à massa muscular;</li>\n                            </ol>\n<h4>Como é usado</h4>\n                            <p> Dose típica:</p>\n                            <ol>\n                                <li>1 scoop (~5 g) por dia;</li>\n                                <li>Misturar com 200–300 ml de água;</li>\n                                <li>Pode tomar a qualquer hora do dia se preferir.</li>\n                            </ol>\n<h4>Importante saber</h4>\n                            <ol>\n                                <li>Beba bastante água durante o dia — creatina puxa água para os músculos.</li>\n                                <li>Não precisa misturar com alimentos açucarados.</li>\n                                <li>Pode ser tomada junto com whey ou outras proteínas.</li>\n                                <li>Resultados aparecem por consistência no uso + treino adequado.</li>\n                            </ol>	creatina	\N	\N	\N	\N	\N	\N	\N	\N
8	usn_creatine_transport_650g	USN CREATINE TRANSPORT 650G	900	img/creatinetransport_650gr-removebg-preview.png	<p>É um suplemento de creatina avançado com carboidratos e aminoácidos projetado para melhorar desempenho muscular, força e energia durante treinos intensos.<br/> Serve para:</p>\n                        <ol>\n                            <li>Aumentar a força e potência;</li>\n                            <li>Melhora desempenho no treino;</li>\n                            <li>Recuperação acelerada entre séries;</li>\n                            <li>Reposição de energia;</li>\n                            <li>Suporte ao ganho de massa magra.</li>\n                        </ol>\n<p>Composição típica:</p>\n                            <ol>\n                                <li>Creatina Monohidratada: forma de creatina muito estudada, ajuda a aumentar a energia armazenada nos músculos;</li>\n                                <li>Carboidratos: fornecem energia rápida e podem melhorar o transporte de creatina para os músculos;</li>\n                                <li>Aminoácidos (como BCAAs): ajudam na recuperação e síntese de proteína muscular;</li>\n                                <li>Eletrólitos e micronutrientes: ajudam com hidratação e função muscular;</li>\n                                <li>Aromatizantes e adoçantes: para sabor.</li>\n                            </ol>\n<h4>Como é usado</h4>\n                            <ol>\n                              \n                                <li>2 scoops (~43 g) por dose;</li>\n                                <li>Misture com 300–350 ml de água fria;</li>\n                               \n                            </ol>\n<h4>Importante saber</h4>\n                            <ol>\n                                <li>Hidratação - Beba água suficiente durante o dia — creatina “puxa” água para as células musculares.</li>\n                                <li>Quem deve ter cuidado \n                                    <br/>Pessoas com problemas renais ou hepáticos devem consultar um médico antes de usar;<br/>\n                                    Se já faz uso de medicamentos, confirme com um profissional de saúde.</li>\n                            </ol>	creatina	\N	\N	\N	\N	\N	\N	\N	\N
9	nutritech_creatine_pure_300g	NUTRITECH CREATINE MONOHYDRATE 300G	1400	img/creatinenutritech_300gr-removebg-preview.png	<p>É um suplemento de creatina monohidratada usado por pessoas que treinam regularmente e querem melhorar força e desempenho. Serve para:</p>\n                            <ol>\n                                <li>Aumentar força e potência muscular – ajuda a produzir energia rápida em exercícios intensos;</li>\n                                <li>Melhora desempenho em treinos curtos e explosivos (como séries de musculação) ao elevar os níveis de fosfocreatina nos músculos;</li>\n                                <li>Acelera recuperação entre séries e treinos pesados;</li>\n                                <li>Apoia aumento de massa magra quando combinado com dieta e treino adequado;</li>\n                                <li>Pode aumentar resistência e explosão muscular em atividades intensas.</li>\n                            </ol>\n<h4>Composição Típica</h4>\n                                <ol>\n                                    <li>Creatina Monohidratada micronizada (~5 g por porção) — forma de creatina muito estudada, dissolução rápida em água e fácil absorção pelo corpo;</li>\n                                    <li>Sem sabor (sem açúcares, sem carboidratos e quase sem calorias);</li>\n                                </ol>\n<h4>Como é usado</h4>\n                                <ol>\n                                \n                                    <li>1 scoop (~5 g) por dia — geralmente 1 a 2 vezes por dia se estiver fazendo carga ou manutenção;</li>\n                                </ol>\n                                <p>Saturação:</p>\n                                <li>20–25 g por dia (5 doses de 5 g) por 5–7 dias;</li>\n                                <li>Depois passam para 5 g por dia como manutenção;</li>\n                                <li>Mas isso não é obrigatório — 5 g diários já funciona bem</li>\n<h4>Importante saber</h4>\n                                <ol>\n                                    <li>Hidrate-se bem durante o dia — a creatina puxa água para os músculos, e isso é normal;</li>\n                                    <li>Pode ser misturada com água, suco ou shake;</li>\n                                    <li>Não contém açúcar ou calorias extras;</li>\n                                    <li>Pode ser usada por iniciantes e avançados, desde que combinada com treino e alimentação.</li>\n                                </ol>	creatina	\N	\N	\N	\N	\N	\N	\N	\N
10	ssa_creatine_supreme_200g	SSA CREATINE MONOHYDRATE  SUPREME 200G	900	img/ssacreatine200gr-removebg-preview.png	<p>É um suplemento de creatina monohidratada micronizada em pó. A creatina é um dos suplementos mais estudados e eficazes para quem faz exercícios intensos, especialmente musculação e treinos explosivos.<br/> Serve para:</p>\n                            <ol>\n                                <li>Aumentar a força e potência;</li>\n                                <li>Melhora desempenho;</li>\n                                <li>Recuperação mais rápida;</li>\n                                <li>Efeitos consistentes com uso contínuo;</li>\n                                <li>Maior massa magra.</li>\n                            </ol>\n<p>Composição Típica:</p>\n                                <ol>\n                                    <li>Creatina monohidratada micronizada (~5 g)<br/>;</li>   \n                                </ol>\n<h4>Como é usado</h4>\n                                <ol>\n                                    <li>Dose diária recomendada - 5gr por dia (1 scoop);</li>\n                                    <li>Misture com 200–300 ml de água ou outra bebida;</li>\n                                    <li>Após o treino – ajuda recuperação;</li>\n                                    <li>Antes do treino – pode dar energia extra;</li>\n                                </ol>\n<h4>Importante saber</h4>\n                                <ol>\n                                    <li>Hidrate-se bem! A creatina puxa água para dentro das células musculares — beber água suficiente é essencial;</li>\n                                    <li>Pode ser misturada com água ou suco;</li>\n                                    <li>Não contém calorias extras, açúcar ou carboidratos;</li>\n                                    <li>Os efeitos dependem de treino, alimentação e uso regular — não é “milagroso”.</li>\n                                </ol>	creatina	\N	\N	\N	\N	\N	\N	\N	\N
11	usn_hardcore_whey_908g	USN HARDCORE WHEY GH 908G	2300	img/whey_908gr-removebg-preview.png	<p>É um suplemento alimentar em pó à base de proteína de soro de leite (whey) combinado com outros ingredientes que podem ajudar no treino, recuperação e ganho de massa muscular. <br/> Este produto foi criado principalmente para quem treina forte e quer:</p>\n                            <ol>\n                                <li>Aumentar a síntese de proteína muscular – ajudando na formação e manutenção dos músculos;</li>\n                                <li>Recuperar mais rápido depois do treino;</li>\n                                <li>Melhorar força e performance em exercícios intensos (devido à creatina);</li>\n                                <li>Possivelmente ajudar a aumentar níveis de hormônio ligados ao crescimento muscular (graças ao Tribulus terrestris e minerais).</li>\n                            </ol>\n<h4>Composição típica</h4>\n                                <ol>\n                                    Uma dose costuma ter cerca de:\n                                    <li>Proteínas\n                                    ~27 g de proteína por dose (~81 g por 100 g)\n                                    • Mistura de whey (concentrado e isolado) e proteína de soja – ajuda a reparar e construir músculos;</li>\n                                    <li>Creatina monohidratada (~3 g por dose): pode ajudar no desempenho em exercícios de alta intensidade;</li>\n                                    <li>Glicina e Taurina: aminoácidos que participam de funções metabólicas e recuperação;</li>\n                                    <li>Tribulus Terrestris (~100 mg por dose): planta usada como suposto “reforço”, embora os efeitos variem;</li>\n                                    <li>Carboidratos e fibras em pequenas quantidades para sabor e absorção.</li>\n                                </ol>\n<h4>Como é usado</h4>\n                                <p>Uso comum recomendado pelo fabricante:</p>\n                                <ol>\n                                    <li>Misture 1 scoop (~33 g) em ~200–300 ml de água ou bebida de sua escolha;</li>\n                                    <li>É comum usar após o treino para ajudar na recuperação muscular;</li>\n                                    <li>Algumas pessoas também usam em outros momentos do dia para alcançar suas necessidades de proteína;</li>\n                                    <li>Consumir 1–2 vezes ao dia.</li>\n                                </ol>\n                                <p><strong>Melhor momento:</strong></p>\n                                <ol>\n                                    <li>Após o treino;</li>\n                                    <li>Ou entre refeições para aumentar calorias.</li>\n                                </ol>\n<h4>Importante saber</h4>\n                                <ol>\n                                    <li>Pode ajudar quando usado junto com treino de força e alimentação equilibrada.</li>\n                                    <li>Não é um substituto de refeições completas.</li>\n                                    <li>Se você for alérgico a leite ou soja, evite ou consulte um profissional de saúde antes.</li>\n                                    <li>\n                                        Efeitos de ingredientes como Tribulus variam de pessoa para pessoa e não são garantidos.\n                                    </li>\n                                </ol>	proteina	\N	\N	\N	\N	\N	\N	\N	\N
12	usn_bluelab_whey_908g	USN BLUELAB WHEY 900G	3000	img/USN_100_BlueLabWhey_908g_Van.webp	<p>É um suplemento de proteína em pó à base de proteína do soro de leite (whey), feito para fornecer proteína de alta qualidade ao corpo — ideal para quem faz musculação e exercícios intensos. Ele combina diferentes tipos de whey (isolado, hidrolisado e concentrado), que são formas de proteína que o corpo usa para recuperar e construir músculos.</p>\n                        <ol>\n                            <li>Fornece proteína de alta qualidade;</li>\n                            <li>Ajuda na recuperação muscular;</li>\n                            <li>Contribui para ganho de massa muscular;</li>\n                            <li>Fácil e rápido de preparar.</li>\n                        </ol>\n<h4>Composição típica (por dose ~150 g)</h4>\n                            <ol>\n                                <li>Blend de proteína de soro de leite (whey): isolado + hidrolisado + concentrado — diferentes formas de proteína com absorção rápida e média.</li>\n                                <li>Aminoácidos essenciais, inclusive BCAAs (5,2-5,5 g por dose), que são importantes para síntese de proteína muscular.</li>\n                                <li>Baixa quantidade de carboidratos e açúcar, o que é bom se o objetivo for focar no proteína em vez de calorias rápidas.</li>\n                                <li>Tolerase™ L (lactase) — enzima que pode ajudar quem tem alguma sensibilidade à lactose.</li>\n                            </ol>\n<h4>Como é usado</h4>\n                            <p>  Geralmente, a recomendação do fabricante é:</p>\n                            <ol>\n                                <li>~Misturar 3 colheres (~150 g) em cerca de 600-650 ml de água;</li>\n                                <li>Tomar 1-2 vezes por dia, entre refeições ou conforme o plano de nutrição;</li>\n                                <li>Pessoas com peso maior podem iniciar com mais porções nos primeiros dias e depois ajustar conforme necessário.</li>\n                            </ol>\n<h4>Importante saber</h4>\n                            <ol>\n                                <li>Funciona bem para quem treina com pesos e quer melhorar recuperação e ganho muscular.</li>\n                                <li>Não é um substituto de refeições completas — deve complementar uma alimentação equilibrada.</li>\n                                <li>Se tiver alergia a leite, cuidado — contém proteína de leite.</li>\n                            </ol>	proteina	\N	\N	\N	\N	\N	\N	\N	\N
13	usn_hydrotech_whey_900g	USN HYDROTECH WHEY 900G	2100	img/wheyhydrotech_900gr-removebg-preview.png	<p>É um suplemento proteico em pó criado especialmente para quem faz treino de musculação ou exercícios intensos. Ele combina proteínas de soro de leite com outras formas para ajudar seu corpo a recuperar e construir músculo depois da atividade física.<br/> Serve para:</p>\n                            <ol>\n                                <li>Ajuda o crescimento e recuperação muscular;</li>\n                                <li>Liberação de proteína em etapas;</li>\n                                <li>Aminoácidos essenciais e BCAAs;</li>\n                                <li>Digestão e absorção facilitadas;</li>\n                                <li>Suporte energético e sistema imunológico.</li>\n                            </ol>\n<p>Composição típica:</p>\n                            <ol>\n                                <li>Energia: ~110–130 kcal;</li>\n                                <li>Proteína: ~22–24 g;</li>\n                                <li>Carboidratos: ~3–6 g;</li>\n                                <li>Açúcares: ~1–3 g;</li>\n                                <li>Gorduras: ~1–2 g;</li>\n                                <li>Sódio: pequena quantidade;</li>\n                                <li>BCAAs naturais do whey: ~4–5 g.</li>\n                            </ol>\n<h4>Como é usado</h4>\n                            <ol>\n                              \n                                <li>Misturar 1 dose (conforme a embalagem) com 250–500 ml de água ou leite;</li>\n                                <li>Tomar após o treino (mais comum) ou entre refeições;</li>\n                                <li>Pessoas com peso maior podem iniciar com menos porções nos primeiros dias e depois ajustar conforme necessário.</li>\n                            </ol>\n<h4>Importante saber</h4>\n                            <ol>\n                                <li>Não é um substituto de uma alimentação balanceada — ele complementa, não substitui refeições completas;</li>\n                                <li>Pessoas com alergia a leite devem evitar ou consultar um profissional de saúde antes de usar;</li>\n                                <li>Os efeitos variam de pessoa para pessoa e dependem também da alimentação e do treino.</li>\n                            </ol>	proteina	\N	\N	\N	\N	\N	\N	\N	\N
14	ssa_whey_isolate_750g	SSA WHEY ISOLATE 750G	3200	img/wheyisolate_750gr-removebg-preview.png	<p>É um suplemento hipercalórico (mass gainer), e o principal objetivo dele é ajudar pessoas a ganhar peso e massa muscular de forma mais rápida e prática.<br/> Serve para:</p>\n                            <ol>\n                                <li>Aumentar a ingestão calórica;</li>\n                                <li>Auxiliar no ganho de massa muscular;</li>\n                                <li>Melhorar a recuperação pós-treino;</li>\n                                <li>Ajudar pessoas com metabolismo acelerado.</li>\n                            </ol>\n<p>Composição Típica:</p>\n                                <ol>\n                                    <li>Proteína de soro de leite isolada (Whey Protein Isolate) – principal ingrediente, com alto teor proteico e rápido aproveitamento pelo corpo, fornecendo aminoácidos essenciais para músculos;</li>\n                                    <li>BCAAs naturais (aminoácidos de cadeia ramificada, como leucina, isoleucina e valina) – ajudam na síntese de proteína e recuperação;</li>\n                                    <li>Saborizantes e aromatizantes – para dar gosto (como chocolate, baunilha, etc.);</li>\n                                    <li>Lecitina de soja ou girassol (ou outro emulsificante) – ajuda o pó a se misturar melhor na água;</li>\n                                    <li>Adoçantes (como sucralose ou equivalente) – para sabor doce sem calorias extras (geral em whey isolate; produto específico pode variar).</li>\n                                </ol>\n<h4>Como é usado</h4>\n                                <ol>\n                                \n                                    <li>1 scoop (~30 g);</li>\n                                    <li>Misturar com 200–300 ml de água;</li>\n                                    <li>Agitar bem por 20–30 segundos.</li>\n                                </ol>\n<h4>Importante saber</h4>\n                                <ol>\n                                    <li>Whey é suplemento, não substitui alimentação equilibrada;</li>\n                                    <li>Beba água suficiente durante o dia;</li>\n                                    <li>Se tiver alergia à proteína do leite, não deve usar;</li>\n                                    <li>Resultados dependem de treino consistente + boa alimentação.</li>\n                                </ol>	proteina	\N	\N	\N	\N	\N	\N	\N	\N
15	npl_platinum_whey+_1kg	NPL PLATINUM WHEY+ 1KG	2500	img/wheyplatinum_1kg-removebg-preview.png	<p>É um suplemento de proteína em pó composto por um mix (“blend”) de diferentes tipos de proteínas de alta qualidade, que são liberadas ao longo do tempo para fornecer aminoácidos continuamente ao corpo.<br/> Serve para:</p>\n                            <ol>\n                                <li>Apoia o crescimento e recuperação muscular;</li>\n                                <li>Liberação contínua de proteínas;</li>\n                                <li>Alta qualidade proteica sem glúten;</li>\n                                <li>Baixo em açúcar;</li>\n                                <li>Versátil no uso.</li>\n                            </ol>\n<h4>Composição Típica</h4>\n                                <p>Cada porção (~40 g) normalmente contém aproximadamente:</p>\n                                <ol>\n                                    <li>Proteína: ~25 g;</li>\n                                    <li>Carboidratos totais: ~6 g;</li>\n                                    <li>Açúcares: ~3,8 g;</li>\n                                    <li>Gorduras: pequena quantidade;</li>\n                                    <li>Energia: ~629 kJ (~150 kcal).</li>\n                                </ol>\n<h4>Como é usado</h4>\n                                <ol>\n                                    <li>Misture 1 scoop (~40 g) com 200–250 ml de água.</li>\n                                    <li>Podem ser 1–3 doses por dia: após treino, entre refeições ou antes da cama\n                                    (a quantidade pode mudar conforme seus objetivos e dieta).</li>\n                                </ol>\n<h4>Importante saber</h4>\n                                <ol>\n                                    <li>Não é medicamento, é suplemento alimentar;</li>\n                                    <li>Funciona melhor quando combinado com treino regular de força e alimentação adequada;</li>\n                                    <li>Pessoas com alergia a leite ou ovo devem evitar ou consultar médico antes.</li>\n                                </ol>	proteina	\N	\N	\N	\N	\N	\N	\N	\N
16	usn-hyperbolic-mass-gh-1kg	USN HYPERBOLIC MASS GH 1KG	800	img/produtos/hyperbolic_1kg-removebg-preview.png	É um suplemento alimentar do tipo hipercalórico (mass gainer), normalmente utilizado por quem tem dificuldade em ganhar peso ou quer aumentar a ingestão calórica para crescimento muscular.\r\nServe para:\r\n\r\n    Aumentar o consumo de calorias diárias;\r\n    Auxiliar no ganho de massa muscular;\r\n    Melhorar a recuperação pós-treino;\r\n\r\nComposição típica (pode variar um pouco, mas geralmente contém:)\r\n\r\n    Carboidratos (60–75%) - Principal fonte de energia;\r\n    Proteína (10–25%) - Pode vir do soro do leite (whey);\r\n    Gorduras (baixa a moderada quantidade) - Auxiliam no aporte calórico;\r\n    Vitaminas e Minerais - Complexo B, Ferro, Zinco, Cálcio\r\n\r\nComo é usado\r\n\r\n    Misturar 1 dose (conforme a embalagem) com 250–500 ml de água ou leite;\r\n    Tomar após o treino (mais comum) ou entre refeições;\r\n    Pessoas com peso maior podem iniciar com menos porções nos primeiros dias e depois ajustar conforme necessário.\r\n\r\nImportante saber\r\n\r\n    Não substitui alimentação sólida;\r\n    Pode causar aumento de gordura se usado em excesso;\r\n    Ideal para quem tem dificuldade real em ganhar peso;\r\n    Deve ser combinado com treino de musculação.\r\n	hipercalorico	\N	\N	f	f	f	0	2026-07-02 06:39:29.616588	2026-07-02 06:39:29.616595
17	ssa-anabolic-muscle-900g	SSA ANABOLIC MUSCLE 900G	700	img/produtos/anabolicmuscle_1kg-removebg-preview.png	É um suplemento do tipo hipercalórico (mass gainer), indicado para quem quer ganhar peso e massa muscular.\r\nPrincipais Benefícios:\r\n\r\n    Ajuda no ganho de massa muscular;\r\n    Aumenta ingestão calórica diária;\r\n    Auxilia na recuperação pós-treino;\r\n    Pode melhorar força e desempenho.\r\n\r\nComposição típica\r\n\r\n    Uma dose costuma ter cerca de:\r\n    Proteína (≈40–50g por dose) - Mistura de whey protein, proteína de soja e outras fontes — ajuda na construção e reparação muscular;\r\n    Carboidratos (≈60–90g por dose) - Geralmente maltodextrina e dextrose — fornecem energia e ajudam a repor o glicogênio muscular;\r\n    Creatina (≈3–5g) - Pode ajudar no aumento de força e desempenho em exercícios intensos;\r\n    Aminoácidos e vitaminas - Apoiam recuperação muscular e metabolismo energético;\r\n    Calorias elevadas - Ideal para quem precisa aumentar a ingestão calórica diária.\r\n\r\nComo é usado\r\n\r\nUso comum recomendado pelo fabricante:\r\n\r\n    Misturar 3–4 colheres (aprox. 150g);\r\n    Adicionar 500–600ml de água ou leite;\r\n    Agitar bem até dissolver;\r\n    Consumir 1–2 vezes ao dia.\r\n\r\nMelhor momento:\r\n\r\n    Após o treino;\r\n    Ou entre refeições para aumentar calorias.\r\n\r\nImportante saber\r\n\r\n    Este tipo de suplemento não substitui uma dieta equilibrada e não faz “milagres”. O ganho de peso/massa depende da sua alimentação e do treino.\r\n    Muitos fabricantes recomendam consultar um profissional de saúde antes de usar, especialmente se você tiver alguma condição médica, for menor de 18 anos ou estiver grávida/nutrindo bebê.\r\n    Suplementos e outros produtos importados podem variar em preço e sabor dependendo do país e fornecedor.\r\n	hipercalorico	\N	\N	f	f	f	0	2026-07-02 06:58:04.334897	2026-07-02 06:58:04.334905
\.


--
-- Data for Name: rating; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rating (id, valor, user_id, produto_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, email, password_hash, phone, reset_code, reset_code_expires, is_admin) FROM stdin;
3	Voyane	voyanerogerio@gmail.com	scrypt:32768:8:1$1VT1pvIvd9g4oSPp$2299b1bd2f43d22e21eb4434e6002e435e74ddc5a0ed3b4b3fa6fbfb9aac60f3cd6bd43f7f9d82ef282cf6c68d59ba8f635b067e4e0917bed74bde40f58c4c3c	845421616	\N	\N	t
4	JS Dev	jsdevtech246@gmail.com	scrypt:32768:8:1$KNQPQEeyNrjY4IF3$50e9a9d325f0c39d0038a132be1ace7221b8fa6fc18555a40c8213f8dcc3ac91ecd21218f2309dc44b7c308f73a88af9d7624e3c04b2cb3b05811411d433f6d4	827570565	\N	\N	f
\.


--
-- Name: cart_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cart_items_id_seq', 8, true);


--
-- Name: carts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.carts_id_seq', 4, true);


--
-- Name: categorias_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categorias_id_seq', 1, false);


--
-- Name: produtos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.produtos_id_seq', 17, true);


--
-- Name: rating_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rating_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: cart_items cart_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_pkey PRIMARY KEY (id);


--
-- Name: carts carts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_pkey PRIMARY KEY (id);


--
-- Name: categorias categorias_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_nome_key UNIQUE (nome);


--
-- Name: categorias categorias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_pkey PRIMARY KEY (id);


--
-- Name: categorias categorias_slug_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_slug_key UNIQUE (slug);


--
-- Name: produtos produtos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produtos
    ADD CONSTRAINT produtos_pkey PRIMARY KEY (id);


--
-- Name: produtos produtos_slug_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produtos
    ADD CONSTRAINT produtos_slug_key UNIQUE (slug);


--
-- Name: rating rating_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT rating_pkey PRIMARY KEY (id);


--
-- Name: cart_items unique_cart_item; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT unique_cart_item UNIQUE (cart_id, produto_id);


--
-- Name: rating unique_user_rating; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT unique_user_rating UNIQUE (user_id, produto_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_carts_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_carts_user_id ON public.carts USING btree (user_id);


--
-- Name: cart_items cart_items_cart_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_cart_id_fkey FOREIGN KEY (cart_id) REFERENCES public.carts(id);


--
-- Name: cart_items cart_items_produto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES public.produtos(id);


--
-- Name: carts carts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: rating rating_produto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT rating_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES public.produtos(id);


--
-- Name: rating rating_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT rating_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict RHf9qM2Ft4QygYp0lxzZ7CBqLW4aRavKpD16q8dw8GGlpCd396PGuThQM3coJfa

