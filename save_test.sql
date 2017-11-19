--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.8
-- Dumped by pg_dump version 9.5.8

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE alembic_version OWNER TO postgres;

--
-- Name: intervention_area; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE intervention_area (
    id integer NOT NULL,
    village_id integer,
    project_id integer,
    date timestamp without time zone
);


ALTER TABLE intervention_area OWNER TO postgres;

--
-- Name: intervention_area_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE intervention_area_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE intervention_area_id_seq OWNER TO postgres;

--
-- Name: intervention_area_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE intervention_area_id_seq OWNED BY intervention_area.id;


--
-- Name: meeting_attendance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE meeting_attendance (
    id integer NOT NULL,
    sg_meeting_id integer,
    member_id integer,
    created_at timestamp without time zone
);


ALTER TABLE meeting_attendance OWNER TO postgres;

--
-- Name: meeting_attendance_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE meeting_attendance_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE meeting_attendance_id_seq OWNER TO postgres;

--
-- Name: meeting_attendance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE meeting_attendance_id_seq OWNED BY meeting_attendance.id;


--
-- Name: member_approved_loan; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE member_approved_loan (
    id integer NOT NULL,
    status integer,
    date timestamp without time zone,
    status_date timestamp without time zone,
    loan_id integer,
    sg_member_id integer
);


ALTER TABLE member_approved_loan OWNER TO postgres;

--
-- Name: member_approved_loan_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE member_approved_loan_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE member_approved_loan_id_seq OWNER TO postgres;

--
-- Name: member_approved_loan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE member_approved_loan_id_seq OWNED BY member_approved_loan.id;


--
-- Name: member_approved_social; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE member_approved_social (
    id integer NOT NULL,
    social_debit_id integer,
    date timestamp without time zone,
    status integer,
    status_date timestamp without time zone,
    sg_member_id integer
);


ALTER TABLE member_approved_social OWNER TO postgres;

--
-- Name: member_approved_social_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE member_approved_social_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE member_approved_social_id_seq OWNER TO postgres;

--
-- Name: member_approved_social_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE member_approved_social_id_seq OWNED BY member_approved_social.id;


--
-- Name: member_fine; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE member_fine (
    id integer NOT NULL,
    status integer,
    type character varying(20),
    amount integer,
    initialization_date timestamp without time zone,
    payment_date timestamp without time zone,
    initiate_by integer,
    wallet_id integer,
    cycle_id integer,
    member_id integer
);


ALTER TABLE member_fine OWNER TO postgres;

--
-- Name: member_fine_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE member_fine_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE member_fine_id_seq OWNER TO postgres;

--
-- Name: member_fine_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE member_fine_id_seq OWNED BY member_fine.id;


--
-- Name: member_loan; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE member_loan (
    id integer NOT NULL,
    amount_loaned double precision,
    request_date timestamp without time zone,
    interest_rate integer,
    initial_date_repayment integer,
    date_payment timestamp without time zone,
    sg_cycle_id integer,
    sg_member_id integer,
    sg_wallet_id integer
);


ALTER TABLE member_loan OWNER TO postgres;

--
-- Name: member_loan_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE member_loan_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE member_loan_id_seq OWNER TO postgres;

--
-- Name: member_loan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE member_loan_id_seq OWNED BY member_loan.id;


--
-- Name: member_social_fund; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE member_social_fund (
    id integer NOT NULL,
    date timestamp without time zone,
    sg_cycle_id integer,
    sg_wallet_id integer,
    amount double precision,
    sg_member_id integer
);


ALTER TABLE member_social_fund OWNER TO postgres;

--
-- Name: member_social_fund_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE member_social_fund_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE member_social_fund_id_seq OWNER TO postgres;

--
-- Name: member_social_fund_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE member_social_fund_id_seq OWNED BY member_social_fund.id;


--
-- Name: members_mini_statement; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE members_mini_statement (
    id integer NOT NULL,
    amount double precision,
    type integer,
    date timestamp without time zone,
    member_id integer
);


ALTER TABLE members_mini_statement OWNER TO postgres;

--
-- Name: members_mini_statement_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE members_mini_statement_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE members_mini_statement_id_seq OWNER TO postgres;

--
-- Name: members_mini_statement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE members_mini_statement_id_seq OWNED BY members_mini_statement.id;


--
-- Name: organization; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE organization (
    id integer NOT NULL,
    name character varying(64),
    type integer,
    email character varying(64),
    phone character varying(30),
    address character varying(180),
    country character varying(120),
    date timestamp without time zone
);


ALTER TABLE organization OWNER TO postgres;

--
-- Name: organization_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE organization_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE organization_id_seq OWNER TO postgres;

--
-- Name: organization_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE organization_id_seq OWNED BY organization.id;


--
-- Name: project; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE project (
    id integer NOT NULL,
    name character varying(100),
    start date,
    "end" date,
    budget double precision,
    donor character varying(240),
    date timestamp without time zone,
    user_id integer,
    organization_id integer,
    partner_id integer
);


ALTER TABLE project OWNER TO postgres;

--
-- Name: project_agent; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE project_agent (
    id integer NOT NULL,
    project_id integer,
    user_id integer,
    date timestamp without time zone
);


ALTER TABLE project_agent OWNER TO postgres;

--
-- Name: project_agent_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE project_agent_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE project_agent_id_seq OWNER TO postgres;

--
-- Name: project_agent_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE project_agent_id_seq OWNED BY project_agent.id;


--
-- Name: project_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE project_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE project_id_seq OWNER TO postgres;

--
-- Name: project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE project_id_seq OWNED BY project.id;


--
-- Name: project_partner; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE project_partner (
    id integer NOT NULL,
    project_id integer,
    partner_id integer,
    date timestamp without time zone
);


ALTER TABLE project_partner OWNER TO postgres;

--
-- Name: project_partner_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE project_partner_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE project_partner_id_seq OWNER TO postgres;

--
-- Name: project_partner_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE project_partner_id_seq OWNED BY project_partner.id;


--
-- Name: saving_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE saving_group (
    id integer NOT NULL,
    name character varying(64),
    creation_date date,
    organization_id integer,
    project_id integer,
    agent_id integer,
    village_id integer,
    status integer
);


ALTER TABLE saving_group OWNER TO postgres;

--
-- Name: saving_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE saving_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE saving_group_id_seq OWNER TO postgres;

--
-- Name: saving_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE saving_group_id_seq OWNED BY saving_group.id;


--
-- Name: saving_group_shares; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE saving_group_shares (
    id integer NOT NULL,
    date timestamp without time zone,
    share integer,
    interest_rate integer,
    max_share integer,
    social_fund integer,
    saving_group_id integer,
    sg_cycle_id integer
);


ALTER TABLE saving_group_shares OWNER TO postgres;

--
-- Name: saving_group_shares_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE saving_group_shares_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE saving_group_shares_id_seq OWNER TO postgres;

--
-- Name: saving_group_shares_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE saving_group_shares_id_seq OWNED BY saving_group_shares.id;


--
-- Name: sg_cycle; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sg_cycle (
    id integer NOT NULL,
    start date,
    "end" date,
    saving_group_id integer,
    active integer
);


ALTER TABLE sg_cycle OWNER TO postgres;

--
-- Name: sg_cycle_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sg_cycle_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sg_cycle_id_seq OWNER TO postgres;

--
-- Name: sg_cycle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sg_cycle_id_seq OWNED BY sg_cycle.id;


--
-- Name: sg_drop_out; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sg_drop_out (
    id integer NOT NULL,
    date timestamp without time zone,
    sg_member_id integer,
    sg_cycle_id integer
);


ALTER TABLE sg_drop_out OWNER TO postgres;

--
-- Name: sg_drop_out_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sg_drop_out_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sg_drop_out_id_seq OWNER TO postgres;

--
-- Name: sg_drop_out_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sg_drop_out_id_seq OWNED BY sg_drop_out.id;


--
-- Name: sg_fin_details; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sg_fin_details (
    id integer NOT NULL,
    name character varying(64),
    type integer,
    account character varying(64),
    saving_group_id integer
);


ALTER TABLE sg_fin_details OWNER TO postgres;

--
-- Name: sg_fin_details_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sg_fin_details_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sg_fin_details_id_seq OWNER TO postgres;

--
-- Name: sg_fin_details_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sg_fin_details_id_seq OWNED BY sg_fin_details.id;


--
-- Name: sg_fines; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sg_fines (
    id integer NOT NULL,
    date timestamp without time zone,
    social_fund integer,
    attendance integer,
    loan integer,
    saving integer,
    meeting integer,
    saving_group_id integer,
    sg_cycle_id integer
);


ALTER TABLE sg_fines OWNER TO postgres;

--
-- Name: sg_fines_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sg_fines_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sg_fines_id_seq OWNER TO postgres;

--
-- Name: sg_fines_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sg_fines_id_seq OWNED BY sg_fines.id;


--
-- Name: sg_meeting; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sg_meeting (
    id integer NOT NULL,
    theme character varying(64),
    meeting_date date,
    created_at timestamp without time zone,
    saving_group_id integer,
    cycle_id integer,
    bank_balance integer,
    external_debt integer
);


ALTER TABLE sg_meeting OWNER TO postgres;

--
-- Name: sg_meeting_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sg_meeting_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sg_meeting_id_seq OWNER TO postgres;

--
-- Name: sg_meeting_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sg_meeting_id_seq OWNED BY sg_meeting.id;


--
-- Name: sg_member; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sg_member (
    id integer NOT NULL,
    user_id integer,
    date timestamp without time zone,
    pin character varying(128),
    admin integer,
    saving_group_id integer
);


ALTER TABLE sg_member OWNER TO postgres;

--
-- Name: sg_member_contributions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sg_member_contributions (
    id integer NOT NULL,
    amount double precision,
    operator integer,
    type integer,
    date timestamp without time zone,
    sg_cycle_id integer,
    sg_wallet_id integer,
    sg_member_id integer
);


ALTER TABLE sg_member_contributions OWNER TO postgres;

--
-- Name: sg_member_contributions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sg_member_contributions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sg_member_contributions_id_seq OWNER TO postgres;

--
-- Name: sg_member_contributions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sg_member_contributions_id_seq OWNED BY sg_member_contributions.id;


--
-- Name: sg_member_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sg_member_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sg_member_id_seq OWNER TO postgres;

--
-- Name: sg_member_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sg_member_id_seq OWNED BY sg_member.id;


--
-- Name: sg_wallet; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sg_wallet (
    id integer NOT NULL,
    amount double precision,
    saving_group_id integer,
    date timestamp without time zone
);


ALTER TABLE sg_wallet OWNER TO postgres;

--
-- Name: sg_wallet_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sg_wallet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sg_wallet_id_seq OWNER TO postgres;

--
-- Name: sg_wallet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sg_wallet_id_seq OWNED BY sg_wallet.id;


--
-- Name: user_fin_details; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE user_fin_details (
    id integer NOT NULL,
    name character varying(64),
    type integer,
    account character varying(64),
    user_id integer
);


ALTER TABLE user_fin_details OWNER TO postgres;

--
-- Name: user_fin_details_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE user_fin_details_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_fin_details_id_seq OWNER TO postgres;

--
-- Name: user_fin_details_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE user_fin_details_id_seq OWNED BY user_fin_details.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE users (
    id integer NOT NULL,
    username character varying(64),
    password_hash character varying(128),
    name character varying(128),
    email character varying(60),
    phone character varying(30),
    type integer,
    organization_id integer,
    education character varying(64),
    first_login integer,
    gender integer,
    location character varying(128),
    date timestamp without time zone,
    confirmation_code character varying(12),
    birth_date date,
    id_number character varying(60)
);


ALTER TABLE users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: village; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE village (
    id integer NOT NULL,
    name character varying(50),
    code character varying(20)
);


ALTER TABLE village OWNER TO postgres;

--
-- Name: village_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE village_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE village_id_seq OWNER TO postgres;

--
-- Name: village_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE village_id_seq OWNED BY village.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY intervention_area ALTER COLUMN id SET DEFAULT nextval('intervention_area_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY meeting_attendance ALTER COLUMN id SET DEFAULT nextval('meeting_attendance_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_approved_loan ALTER COLUMN id SET DEFAULT nextval('member_approved_loan_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_approved_social ALTER COLUMN id SET DEFAULT nextval('member_approved_social_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_fine ALTER COLUMN id SET DEFAULT nextval('member_fine_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_loan ALTER COLUMN id SET DEFAULT nextval('member_loan_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_social_fund ALTER COLUMN id SET DEFAULT nextval('member_social_fund_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY members_mini_statement ALTER COLUMN id SET DEFAULT nextval('members_mini_statement_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY organization ALTER COLUMN id SET DEFAULT nextval('organization_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY project ALTER COLUMN id SET DEFAULT nextval('project_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY project_agent ALTER COLUMN id SET DEFAULT nextval('project_agent_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY project_partner ALTER COLUMN id SET DEFAULT nextval('project_partner_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY saving_group ALTER COLUMN id SET DEFAULT nextval('saving_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY saving_group_shares ALTER COLUMN id SET DEFAULT nextval('saving_group_shares_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_cycle ALTER COLUMN id SET DEFAULT nextval('sg_cycle_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_drop_out ALTER COLUMN id SET DEFAULT nextval('sg_drop_out_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_fin_details ALTER COLUMN id SET DEFAULT nextval('sg_fin_details_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_fines ALTER COLUMN id SET DEFAULT nextval('sg_fines_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_meeting ALTER COLUMN id SET DEFAULT nextval('sg_meeting_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_member ALTER COLUMN id SET DEFAULT nextval('sg_member_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_member_contributions ALTER COLUMN id SET DEFAULT nextval('sg_member_contributions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_wallet ALTER COLUMN id SET DEFAULT nextval('sg_wallet_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_fin_details ALTER COLUMN id SET DEFAULT nextval('user_fin_details_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY village ALTER COLUMN id SET DEFAULT nextval('village_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY alembic_version (version_num) FROM stdin;
772c70619184
\.


--
-- Data for Name: intervention_area; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY intervention_area (id, village_id, project_id, date) FROM stdin;
2	2	3	2017-08-16 09:50:41.768641
1	1	3	2017-08-16 09:50:41.807458
\.


--
-- Name: intervention_area_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('intervention_area_id_seq', 2, true);


--
-- Data for Name: meeting_attendance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY meeting_attendance (id, sg_meeting_id, member_id, created_at) FROM stdin;
1	1	3	2017-10-29 17:59:40.356469
2	1	5	2017-10-29 17:59:40.356469
4	1	6	2017-10-29 18:15:07.967446
5	1	4	2017-10-29 18:15:07.967446
\.


--
-- Name: meeting_attendance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('meeting_attendance_id_seq', 5, true);


--
-- Data for Name: member_approved_loan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY member_approved_loan (id, status, date, status_date, loan_id, sg_member_id) FROM stdin;
1	0	2017-09-13 17:20:45.150793	2017-09-18 17:47:35.286287	1	3
2	1	2017-09-19 13:53:56.777798	2017-09-19 14:02:10.534513	2	3
3	2	2017-10-19 17:13:48.390625	\N	3	3
5	2	2017-10-19 17:13:48.384889	\N	4	3
7	2	2017-10-19 17:13:48.390625	\N	5	3
8	2	2017-10-19 17:13:48.390625	\N	5	4
4	1	2017-10-19 17:13:48.390625	2017-10-23 15:54:15.695683	3	4
6	1	2017-10-19 17:13:48.384889	2017-10-26 19:31:34.938149	4	4
9	2	2017-10-26 16:55:06.568611	\N	6	3
10	2	2017-10-26 16:55:06.568611	\N	6	4
11	2	2017-10-26 16:55:06.57664	\N	7	3
12	2	2017-10-26 16:55:06.57664	\N	7	4
13	2	2017-11-06 20:32:28.738355	\N	8	3
14	2	2017-11-06 20:32:28.738355	\N	8	4
15	2	2017-11-07 13:42:42.588499	\N	9	3
16	2	2017-11-07 13:42:42.588499	\N	9	4
\.


--
-- Name: member_approved_loan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('member_approved_loan_id_seq', 16, true);


--
-- Data for Name: member_approved_social; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY member_approved_social (id, social_debit_id, date, status, status_date, sg_member_id) FROM stdin;
1	1	2017-09-18 16:16:07.337301	0	2017-09-18 17:46:27.911233	\N
2	2	2017-10-18 17:49:35.574388	2	\N	3
3	3	2017-10-18 17:49:35.566901	2	\N	3
4	4	2017-10-19 17:13:48.155394	2	\N	3
6	5	2017-10-19 17:13:48.400898	2	\N	3
7	5	2017-10-19 17:13:48.400898	1	2017-10-23 16:05:59.890467	4
5	4	2017-10-19 17:13:48.155394	1	2017-10-26 19:38:38.569405	4
8	6	2017-10-26 16:55:06.579134	2	\N	3
9	6	2017-10-26 16:55:06.579134	2	\N	4
10	7	2017-11-06 20:32:28.73686	2	\N	3
11	7	2017-11-06 20:32:28.73686	2	\N	4
\.


--
-- Name: member_approved_social_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('member_approved_social_id_seq', 11, true);


--
-- Data for Name: member_fine; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY member_fine (id, status, type, amount, initialization_date, payment_date, initiate_by, wallet_id, cycle_id, member_id) FROM stdin;
1	0	social_fund_fine	100	2017-09-25 10:32:08.287807	\N	3	7	10	\N
\.


--
-- Name: member_fine_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('member_fine_id_seq', 1, true);


--
-- Data for Name: member_loan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY member_loan (id, amount_loaned, request_date, interest_rate, initial_date_repayment, date_payment, sg_cycle_id, sg_member_id, sg_wallet_id) FROM stdin;
1	25000	2017-09-13 17:20:45.14555	10	25	\N	7	1	4
2	25000	2017-09-19 13:53:56.773536	10	25	\N	7	1	4
3	1000	2017-10-19 17:13:48.37787	10	25	\N	10	4	7
4	1000	2017-10-19 17:13:48.371767	10	0	\N	10	4	7
5	5000	2017-10-19 17:13:48.37787	10	50	\N	10	4	7
6	1000	2017-10-26 16:55:06.552047	10	1000	\N	10	4	7
7	1000	2017-10-26 16:55:06.561243	10	1000	\N	10	4	7
8	300	2017-11-06 20:32:28.733594	10	12	\N	10	15	7
9	1500	2017-11-07 13:42:42.575999	10	123	\N	10	4	7
\.


--
-- Name: member_loan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('member_loan_id_seq', 9, true);


--
-- Data for Name: member_social_fund; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY member_social_fund (id, date, sg_cycle_id, sg_wallet_id, amount, sg_member_id) FROM stdin;
1	2017-09-18 16:16:07.329226	7	4	12000	\N
2	2017-10-18 17:49:35.562117	10	7	1000	4
3	2017-10-18 17:49:35.562499	10	7	1000	4
4	2017-10-19 17:13:48.141705	10	7	4000	4
5	2017-10-19 17:13:48.388339	10	7	35000	4
6	2017-10-26 16:55:06.574669	10	7	1000	4
7	2017-11-06 20:32:28.732995	10	7	100	4
\.


--
-- Name: member_social_fund_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('member_social_fund_id_seq', 7, true);


--
-- Data for Name: members_mini_statement; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY members_mini_statement (id, amount, type, date, member_id) FROM stdin;
1	19000	1	2017-10-07 16:47:33.322053	4
2	1000	2	2017-10-07 16:50:53.010116	4
3	12500	1	2017-10-07 17:08:18.866572	3
\.


--
-- Name: members_mini_statement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('members_mini_statement_id_seq', 3, true);


--
-- Data for Name: organization; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY organization (id, name, type, email, phone, address, country, date) FROM stdin;
1	save	3	info@getsave.io	250785383100	Kacyiru KG 578 ST	Rwanda	2017-08-11 09:40:16.508226
5	Exuus12	3	info@exuus123.com	250789876	Kacyiru KG 12st	Rwanda	2017-08-11 10:44:44.090842
6	Exuus2	3	info@exuus23.com	250789876	Kacyiru KG 12st	Rwanda	2017-08-11 10:44:44.090842
2	Exuus edited	3	info@exuus.com	250789876	Kacyiru KG 12st	Rwanda	2017-08-11 10:44:44.090842
\.


--
-- Name: organization_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('organization_id_seq', 6, true);


--
-- Data for Name: project; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY project (id, name, start, "end", budget, donor, date, user_id, organization_id, partner_id) FROM stdin;
1	kuraneza	2017-04-08	2017-12-12	12000000	HOPE	2017-08-11 10:44:44.101584	1	1	\N
2	cartix.io	2015-12-08	2015-12-12	21000	AFR	2017-08-11 16:15:43.091038	2	1	\N
3	save sgs	2017-12-09	2017-12-10	1200000900	Exuus	2017-08-15 15:16:18.018502	1	1	\N
\.


--
-- Data for Name: project_agent; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY project_agent (id, project_id, user_id, date) FROM stdin;
1	1	4	2017-11-12 20:21:07.622314
\.


--
-- Name: project_agent_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('project_agent_id_seq', 1, true);


--
-- Name: project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('project_id_seq', 3, true);


--
-- Data for Name: project_partner; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY project_partner (id, project_id, partner_id, date) FROM stdin;
\.


--
-- Name: project_partner_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('project_partner_id_seq', 1, false);


--
-- Data for Name: saving_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY saving_group (id, name, creation_date, organization_id, project_id, agent_id, village_id, status) FROM stdin;
1	Exuus SG_5	2017-06-18	1	1	1	1	\N
2	Crew sg	2017-06-18	1	1	1	1	\N
3	Guillaume's Group	2017-06-18	1	1	1	1	\N
4	Guillaume's Group 2	2017-06-18	1	2	2	1	\N
5	Group A	2017-12-12	1	1	1	1	1
6	SG Mania	2012-05-09	1	1	1	1	1
7	SG Maniaccc	2012-05-09	1	1	1	1	1
16	Group AFV	2033-12-12	2	2	2	2	0
19	The Marriott Group	2030-12-12	1	2	2	1	0
29	DAMARARA	1212-12-12	\N	2	2	2	1
30	Steve's Group	1212-12-12	\N	2	2	2	1
31	Kandagira Group	1212-12-12	\N	2	2	3	1
32	Prometeus	2018-12-12	\N	2	2	2	1
33	Group Sixela	1212-12-12	\N	1	4	2	0
34	Group Muhire	1212-12-12	\N	1	4	3	1
35	ABC Group	1212-12-12	\N	1	4	2	0
36	Cedric Group	1212-12-12	\N	1	4	2	1
\.


--
-- Name: saving_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('saving_group_id_seq', 36, true);


--
-- Data for Name: saving_group_shares; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY saving_group_shares (id, date, share, interest_rate, max_share, social_fund, saving_group_id, sg_cycle_id) FROM stdin;
1	2017-09-25 09:03:13.266424	300	50	5000	500	6	10
3	2017-10-07 14:29:04.883284	4500	50	5000	4500	7	11
4	2017-11-11 17:12:46.043966	4500	45	2300	50000	29	13
5	2017-11-11 17:09:42.380824	45	43	4500	34566	30	14
6	2017-11-11 17:12:46.043966	500	4560	234234	4560	31	15
7	2017-11-12 07:23:27.014612	5000	123	3400	21441	32	16
8	2017-11-13 16:18:03.97554	560	50	500	5	33	17
9	2017-11-13 16:29:04.157824	2000	50	12312	123123	34	18
10	2017-11-13 16:18:03.97554	23423	234	234	234	35	19
11	2017-11-13 17:48:06.446804	500	500	54354	34534	36	20
\.


--
-- Name: saving_group_shares_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('saving_group_shares_id_seq', 11, true);


--
-- Data for Name: sg_cycle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sg_cycle (id, start, "end", saving_group_id, active) FROM stdin;
7	2017-02-21	2017-03-22	1	1
8	2017-01-30	2017-12-31	2	1
9	2017-09-20	2017-12-20	5	1
10	2017-09-20	2017-12-20	6	1
11	2017-09-10	2017-12-20	7	1
12	2017-10-07	2018-02-07	19	1
13	2017-11-11	2018-05-11	29	1
14	2017-11-11	2018-05-11	30	1
15	2017-11-11	2018-05-11	31	1
16	2017-11-12	2018-05-12	32	1
17	2017-11-13	2018-05-13	33	1
18	2017-11-13	2018-05-13	34	1
19	2017-11-13	2018-07-13	35	1
20	2017-11-13	2018-05-13	36	1
\.


--
-- Name: sg_cycle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sg_cycle_id_seq', 20, true);


--
-- Data for Name: sg_drop_out; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sg_drop_out (id, date, sg_member_id, sg_cycle_id) FROM stdin;
\.


--
-- Name: sg_drop_out_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sg_drop_out_id_seq', 1, false);


--
-- Data for Name: sg_fin_details; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sg_fin_details (id, name, type, account, saving_group_id) FROM stdin;
1	Bank of Rwanda	1	234234234234	5
2	BRD	1	234234234	5
3	Bank of Rwanda	1	234234234	6
4	Bank of Uganda	1	234234234234	6
5	Bank of Rwanda	1	234234234	7
6	Bank of Uganda	1	234234234234	7
7	Bank of Kigali	4	234234234	29
8	Bank of Rwanda	4	23423423423	30
9	Bank of Rwanda	4	23423423423	31
10	Bank of Rwanda	3	2423243423	32
11	Bank of Rwanda	3	3242423423	33
12	Bank A	3	234234234234	34
13	Bank AAA	3	324234	35
14	Bank A	3	23423423	36
\.


--
-- Name: sg_fin_details_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sg_fin_details_id_seq', 14, true);


--
-- Data for Name: sg_fines; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sg_fines (id, date, social_fund, attendance, loan, saving, meeting, saving_group_id, sg_cycle_id) FROM stdin;
1	2017-09-25 09:03:13.250496	100	100	50	200	100	6	10
4	2017-10-07 14:29:04.878783	4050	23444	50	23423	4444	7	11
5	2017-11-11 17:12:46.035922	300	3000	50	234234	3000	29	13
6	2017-11-11 17:09:42.376041	5000	4500	50	2300	3000	30	14
7	2017-11-11 17:12:46.035922	4500	4500	50	3400	5555	31	15
8	2017-11-12 07:23:27.010232	4500	2000	50	4500	1000	32	16
9	2017-11-13 16:18:03.968079	5000	500	50	1000	5000	33	17
10	2017-11-13 16:29:04.145694	4500	400	50	6000	4444	34	18
11	2017-11-13 16:18:03.968079	400	4000	50	342423	342432	35	19
12	2017-11-13 17:48:06.439064	4340	34324	50	43444	4000	36	20
\.


--
-- Name: sg_fines_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sg_fines_id_seq', 12, true);


--
-- Data for Name: sg_meeting; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sg_meeting (id, theme, meeting_date, created_at, saving_group_id, cycle_id, bank_balance, external_debt) FROM stdin;
1	Inama Ya SG	2017-12-06	2017-10-29 17:44:04.714784	6	10	\N	\N
2	Guil	1212-12-12	2017-10-29 20:18:43.710016	2	8	\N	\N
3	Theme A	1212-12-12	2017-10-29 20:18:43.710016	2	8	\N	\N
4	Theme Monday	1212-12-12	2017-10-29 23:11:41.206297	1	7	49999	56000
5	Theme A	2019-12-12	2017-10-30 09:55:18.38817	1	7	50000	50000
6	Theme Inka	2019-12-12	2017-10-30 09:55:18.38817	1	7	50000	50000
7	Isangano	2012-12-12	2017-10-30 09:55:18.38817	2	8	560000	459888
8	Isangano	2012-12-12	2017-10-30 09:55:18.38817	2	8	560000	459888
9	Theme U Rwanda	2018-12-12	2017-10-30 09:55:18.38817	2	8	45000	20000
10	serkjfsu	1212-12-12	2017-11-13 21:08:12.334835	4	\N	2342	432423
11	Iname y' akarere	2011-11-11	2017-11-13 21:08:07.071727	4	\N	2323	3232
12	Kuzigama	1212-12-12	2017-11-13 21:08:12.334835	4	\N	23423	23423
13	Kuzigama	1212-12-12	2017-11-13 21:08:12.334835	32	16	23423	23423
14	Inama A	1212-12-12	2017-11-14 11:09:44.168912	16	\N	5600	345552
\.


--
-- Name: sg_meeting_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sg_meeting_id_seq', 14, true);


--
-- Data for Name: sg_member; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sg_member (id, user_id, date, pin, admin, saving_group_id) FROM stdin;
2	2	2017-09-04 17:25:34.581425	pbkdf2:sha256:50000$scawvDUP$f827dc4e2b03964c51d1aa757af0656039d666b5d2c907f7398e507af0c25297	\N	2
1	2	2017-08-31 10:35:16.901891	pbkdf2:sha256:50000$EEsNGOgN$6cc037c25de2504bf0b0091ec54d2d17ee114c24077304e7c6eabebe37bddbc9	\N	1
3	8	2017-09-13 17:20:46.022638	pbkdf2:sha256:50000$JQTE6K52$f3dc140d8c4552d8d1cf0f03f23f505f209eafe78e623bd1016b0cf3ce2f8b9c	1	6
5	48	2017-10-18 09:12:07.33799	pbkdf2:sha256:50000$UOMjjMTF$83921bcea43fb57071ff54da9bb2bb35680bac54f2744b8c82dbcad02d11659f	0	6
4	22	2017-09-20 14:24:30.318781	pbkdf2:sha256:50000$3fDDU62y$e349858d0fe4c3f999a9b525d52e2dc5c3bad904951b490f289adc4ff8da59b2	1	6
6	49	2017-10-18 17:49:35.623365	pbkdf2:sha256:50000$FERmEZNS$a8ae0e56b6802daf210c3fc2e233213226e38f9baa6a67bc0a4226cfa1dcbe90	0	6
7	55	2017-10-19 08:26:48.476608	pbkdf2:sha256:50000$ScssO8UB$26864bba2e2b795fcc6bc41d9c677296d5d0b3af282821ec14a84f1e9882494f	0	6
8	73	2017-10-19 17:13:48.449518	\N	0	6
9	95	2017-10-22 19:41:21.322087	\N	1	2
10	97	2017-10-26 15:05:37.255907	\N	1	2
11	99	2017-10-26 15:05:37.259932	\N	1	1
13	101	2017-10-26 15:59:12.613982	\N	1	2
14	104	2017-10-26 15:59:12.613982	\N	1	2
15	105	2017-10-26 16:55:06.647871	pbkdf2:sha256:50000$fj47u6NI$299eebd265e8312007a21fed41d7b58628008db159db2c485f9424a70c871712	0	6
17	107	2017-11-07 13:42:42.647159	\N	0	6
18	121	2017-11-13 17:48:05.667171	\N	0	4
19	123	2017-11-13 17:50:10.245782	\N	0	4
20	124	2017-11-13 21:08:06.926776	\N	1	16
16	106	2017-11-07 13:42:42.650984	pbkdf2:sha256:50000$b27GdaRm$9395095955898098874dfc68dddabd476f20404661e877c54818aa8781ee2496	0	6
21	126	2017-11-14 11:09:44.147328	\N	1	16
22	128	2017-11-13 21:08:12.308835	\N	0	4
\.


--
-- Data for Name: sg_member_contributions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sg_member_contributions (id, amount, operator, type, date, sg_cycle_id, sg_wallet_id, sg_member_id) FROM stdin;
1	1500	1	1	2017-09-04 17:49:49.400405	8	\N	\N
2	2300	1	1	2017-09-04 18:33:09.684627	8	\N	\N
3	300	1	2	2017-09-04 19:09:52.002407	8	\N	\N
4	19000	1	1	2017-10-07 16:47:33.228863	10	7	4
5	1000	1	2	2017-10-07 16:50:52.964183	10	7	4
6	12500	1	1	2017-10-07 17:08:18.820921	10	7	3
\.


--
-- Name: sg_member_contributions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sg_member_contributions_id_seq', 6, true);


--
-- Name: sg_member_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sg_member_id_seq', 22, true);


--
-- Data for Name: sg_wallet; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sg_wallet (id, amount, saving_group_id, date) FROM stdin;
1	4100	2	2017-09-04 17:25:34.556688
2	0	3	2017-09-06 09:48:00.979874
3	0	4	2017-09-06 09:48:00.973052
4	0	1	2017-09-19 12:47:15.23782
6	0	5	2017-09-20 21:39:15.966
8	0	7	2017-10-07 14:29:04.85296
9	0	16	2017-10-07 14:56:51.315074
10	0	19	2017-10-07 16:36:14.36268
7	32500	6	2017-09-25 09:03:13.180413
11	0	29	2017-11-11 17:12:45.98829
12	0	30	2017-11-11 17:09:42.347463
13	0	31	2017-11-11 17:12:45.98829
14	0	32	2017-11-12 07:23:26.984812
15	0	33	2017-11-13 16:18:03.922945
16	0	34	2017-11-13 16:29:04.080994
17	0	35	2017-11-13 16:18:03.922945
18	0	36	2017-11-13 17:48:06.380243
\.


--
-- Name: sg_wallet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sg_wallet_id_seq', 18, true);


--
-- Data for Name: user_fin_details; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY user_fin_details (id, name, type, account, user_id) FROM stdin;
1	GT BANK	1	17887988298899	4
\.


--
-- Name: user_fin_details_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('user_fin_details_id_seq', 1, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY users (id, username, password_hash, name, email, phone, type, organization_id, education, first_login, gender, location, date, confirmation_code, birth_date, id_number) FROM stdin;
1	rmuhire	pbkdf2:sha256:50000$RwNSRKFe$009f586b8b23b94276222cfceb17ca531b0a93d2af1e18ad85e501303c1519b2	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
4	guillaume	pbkdf2:sha256:50000$d3jZ91wR$6c97f0c01de26968a6b576331d63160103f32e3937ca5582eb741d348a813e48	Guillaume Sayinzoga	guillaumesayinzoga@gmail.com	+25078888878	2	1	University	1	3	Kacyiru	2017-08-15 17:36:10.707631	107-325-446	1992-12-12	555555555
3	Luc	pbkdf2:sha256:50000$PkNLewR3$e3c4f87756a17dae70d0cbcfde242754e646462507683dcaa449293c9216702a	Luc	Luc@gmail.com	250789265812	3	1	\N	\N	\N	\N	\N	\N	\N	\N
69	EE22813	pbkdf2:sha256:50000$nVfI28go$019577512a2a3a2bd2eaa53658461399c7e2ba0e8765732ed749e87b2ea092d0	E222	EE22310@getsave.io	123334444	3	2		1	1	no location	2017-10-19 17:13:48.324218	938-353-717	2017-11-11	32423423423423424
70	wwe3927	pbkdf2:sha256:50000$HqMz9Khh$b2797f3f08cb041ac023641e47c4b395501ba4cee99e9d9a871650d7c37991f9	we34343	wwe3374@getsave.io	1221312312	3	2		1	1	no location	2017-10-19 17:13:48.246082	584-74-82	1212-12-12	3433434333433
71	wwer417	pbkdf2:sha256:50000$kdqEC1KT$211ba1b06789e1982eceddd1d4b25956cca2b3dc23793464e5d0433655bf6a17	werwerm3434	wwer333@getsave.io	12312331323	3	1		1	0	no location	2017-10-19 17:13:48.246082	584-74-82	1212-12-12	34534222333222
72	GGui288	pbkdf2:sha256:50000$antDRXv4$0fd5c7f6f5c1b5c28776b66a4439e6043ece450af3b19c25d535e517f28266f4	Guiallasdka	GGui605@getsave.io	123122412412	3	1		1	1	no location	2017-10-19 17:13:48.051562	861-392-755	2018-12-12	23423423
73	rwagasore	pbkdf2:sha256:50000$hx6dMpZG$46e3ec9d5af611369ee4d3c78351b69907f2fc4e12547dc6128e1eb519144513	Eugene	rwagasore@gmail.com	250789385878	3	1	Bachelor	1	0	no location	2017-10-19 17:13:48.324218	938-353-717	1991-01-01	123456600
74	GGui791	pbkdf2:sha256:50000$q6htkrvG$0e5ab6d03bedb6901fc17c5af8f99ef5c5bcf01254496b937fb4392962668ab5	Guiasd223	GGui998@getsave.io	12312312312	3	1		1	0	no location	2017-10-19 17:13:48.051562	861-392-755	1212-12-12	2323323423
75	eewe601	pbkdf2:sha256:50000$brwZuuBo$9d191ac8f7b58effa2c2c63ab69a332a0d7c9376c46b0e0bf97f1497b59acfa8	ewedw23	eewe718@getsave.io	12312312	3	2		1	0	no location	2017-10-19 17:13:48.324218	938-353-717	1212-12-12	2342342342342
76	wwee573	pbkdf2:sha256:50000$fJyAkzLL$6e57d1fbce76e875b78c723e4b34d3e3da59d7fb55fd1986d09d921420ee04f3	weew234wdsa	wwee975@getsave.io	123331334444	3	2		1	0	no location	2017-10-19 17:13:48.246082	584-74-82	1212-12-12	23454323321
77	oohv820	pbkdf2:sha256:50000$LDiMj0MG$7e8fede767bfe607163bf83ee69eac8ac383acc225d7332c363c7b3808a12376	ohvghkjn	oohv432@getsave.io	1212123123321	3	1		1	0	no location	2017-10-19 17:13:48.051562	861-392-755	1212-12-12	98765435678
78	ssdf634	pbkdf2:sha256:50000$mUeDDgE8$56afa44085526110824a498f8ab3906961aa3d25567729c197785fe6af1633a3	sdf2342sfd	ssdf840@getsave.io	234234234	3	1		1	0	no location	2017-10-22 18:55:20.249528	78-988-943	1010-10-21	23456576567
79	SSFD813	pbkdf2:sha256:50000$LVdSgu4V$99bcc11f51641704cbd59a0bc861f0fb15a533ea69fb6a01a159c7e06aedc953	SFD34	SSFD559@getsave.io	1231243123	3	1		1	0	no location	2017-10-22 18:55:20.249528	78-988-943	1212-12-12	23423423423423
80	SSFD428	pbkdf2:sha256:50000$sd8YfjDH$6b851da1bef751e3f4803dd19120de53d36c7e9d351ef0c830f5be43edb1935b	SFDSDFS	SSFD500@getsave.io	2131231231	3	1		1	1	no location	2017-10-19 17:13:48.329958	211-875-741	1212-12-12	232342342342
82	aasd009	pbkdf2:sha256:50000$XiYlStfL$147f23209cbf11035ba6876a830795a615dffea4dad6cbccf80bd4d894bef33a	asdasdasd	aasd675@getsave.io	9876545	3	1		1	0	no location	2017-10-19 17:13:48.329958	211-875-741	2017-12-12	876234234234
32	uSerNamE	pbkdf2:sha256:50000$Puc4iJfX$9448928a39be117beaa983236749b20d5277ffbc246622f16539327fb98ce95f	SAYINZOGA GUILLAUME	giills@gmail.com	788737814	3	2	EdUcAtIoN	1	0	no location	2017-10-15 22:00:46.382235	813-441-38	2016-12-12	234234
33		pbkdf2:sha256:50000$Evccf86p$e8aa85212c6ee27a3768d37fa46ebceacbd960207575bb5ad121db1a0a251c31	John doe	JOHN@gmail.com	908876543	3	2		1	0	no location	2017-10-15 22:00:46.6408	209-195-304	1212-12-12	976767
36	Uxx	pbkdf2:sha256:50000$pdFxsGza$e67f212dbf481cec07806c1b1001a0fb2661b5bfd47bd509f89310bdb087d9c2	UGHH	gjfd@gmail.com	234234	3	1		1	1	no location	2017-10-15 22:09:32.115534	407-320-693	2016-12-12	234322
40	String(TempUserName)	pbkdf2:sha256:50000$QTuQb8Ou$88779ce4db4547b3c7df7cd0de41b51ca4bbfd53831f42a4866c6b3e1901b03f	BelX	belxxx@free.fgh	99999	3	1		1	1	no location	2017-10-15 22:18:47.93863	646-152-144	2019-12-12	3224443444
42	GGbb015	pbkdf2:sha256:50000$YvE5FNAd$0c317a0bced8ad495b54830aa8c040a5b16f7ac715b3dc29b0294ee0848715c3	Gbbvv	GGbb660@getsave.io	123123123	3	1		1	1	no location	2017-10-15 22:32:47.733215	909-55-797	1212-12-12	2344442
43	WWER540	pbkdf2:sha256:50000$15YwJMUm$eb9f208043d785d8702b4a70b496568e35d1933a6d650a2ef69c02f0dc873929	WERR	WWER544@getsave.io	1235423423	3	2		1	1	no location	2017-10-15 22:32:44.097658	169-882-551	2019-11-11	23424234
8	kenessa	pbkdf2:sha256:50000$PJtWFTAh$caa8e37776b1c2313f98e61c2614debe30de724a82a8a2a6ed8c7ae8f1c775f3	Kenessa	kenessa@gmail.com	250785383100	3	1	A-level	1	1	\N	2017-09-13 17:20:45.123066	257-880-958	1900-06-18	\N
47	FFSD149	pbkdf2:sha256:50000$2C6PH1UI$9d2f08e8cb18d72dff42e2f2b0bc2908e842c7953f42ae69af18a250ce541bb2	FSDFS	FFSD578@getsave.io	1231333	3	1		1	1	no location	2017-10-16 10:27:31.136831	476-92-923	2018-12-12	23423
48	sshema	pbkdf2:sha256:50000$NMfJ7tWh$e070151a43dbec35dfbf06e49164421f152dada0e9c9036489c7b4b454048bae	Steve Shema	sshema@exuus.com	250788304273	3	1	Bachelor	1	0	no location	2017-10-18 09:12:07.291927	601-98-596	1991-01-01	1234566
22	stanlem	pbkdf2:sha256:50000$LYu9g4I2$a80f4d0d0db3a53e2ca20a6f474c53b268f4235731ad5a6c1e94a631db791966	Stanley Mwizera	mwizerwa77@gmail.com	250788683008	3	1	MASTER	1	0	\N	2017-09-20 14:24:30.168649	451-236-253	1991-01-01	\N
49	ltuyi	pbkdf2:sha256:50000$QTiOTxDz$63cb6af09ed4a9d1191067d1d647da07a57502481f5501e42710d679dd32149b	Luc Tuyishime	ltuyishime@exuus.com	250784421255	3	1	Bachelor	1	0	no location	2017-10-18 17:49:35.489836	289-852-464	1991-01-01	12345663
55	dasixela	pbkdf2:sha256:50000$8QvBnLEj$81396fd35e1ea080b93bb5dcd90418389d967cb7748b0644d95a07e98afd636a	David Sixela	dsixela@exuus.com	250723729155	3	1	Bachelor	1	0	no location	2017-10-19 08:26:48.455575	162-313-123	1991-01-01	123456632
56	ssdf678	pbkdf2:sha256:50000$vJVbqZbA$6c69fdc514cd37039cfa1c24f48f28f34c4ab42c69717f5c09c73779641f591b	sdf44	ssdf899@getsave.io	1434234	3	2		1	1	no location	2017-10-19 17:13:48.051562	861-392-755	2014-12-12	234
61	aasd748	pbkdf2:sha256:50000$L3QYNTUZ$272dcd9b9e2d5b10907c1e7e411c1259317d808fd4f393dd6491bb56425192d5	asd23d2d	aasd115@getsave.io	123123	3	2		1	1	no location	2017-10-19 17:13:48.246082	584-74-82	2017-12-12	234234123123123
88	AASF278	pbkdf2:sha256:50000$mx47jf8q$1dae258f73e8454e943212a8e43dafbb2b4873033c43ab9f9594770044a76889	ASFDSA	AASF274@getsave.io	12312412312	3	1		1	0	no location	2017-10-22 18:55:20.249528	78-988-943	1212-12-12	31234234234
86	JJAr660	pbkdf2:sha256:50000$TTaZ6WBt$1b4c963a9ee8016c2232ef4756aaa23ad1fd99baa2eca71c6012e0ee9179ec5e	JAredasd	JJAr687@getsave.io	12312312123	3	2		1	1	no location	2017-10-19 17:13:48.246082	584-74-82	2018-10-10	234234231233
87	GGAS593	pbkdf2:sha256:50000$Uj36Gr79$a87967f8c970bc1d62f7d64b1b30ef77b624ababbb210ae22b58fc487d385dec	GASDAS	GGAS258@getsave.io	12333421211	3	2		1	0	no location	2017-10-19 17:13:48.329958	211-875-741	2018-12-12	12312312
89	SSDF062	pbkdf2:sha256:50000$icFsd5M9$14e8ebd4793a5724f331762e644b093e6a10382b9ba416fa87e1b0255a5c36f6	SDFSDF	SSDF965@getsave.io	123124142124	3	2		1	0	no location	2017-10-22 19:35:34.296296	766-824-617	2019-12-12	2342342342323
93	AADS384	pbkdf2:sha256:50000$hwfyS1AQ$8b81351da76ad37cf635fa82b7b1bb07f4d682bf7b0099c72440439af9b4a24a	ADSASD	AADS982@getsave.io	12333324114	3	1		1	0	no location	2017-10-22 19:41:21.259503	243-284-196	2018-12-12	234234234353
94	2234092	pbkdf2:sha256:50000$9grgT8Ax$4f79f45bee290ee910a338e0624366cb7b6f442cb57781af46b6fa80f96c7d9f	234233234	2234229@getsave.io	1231323123123	3	1		1	0	no location	2017-10-22 19:41:24.075803	418-806-605	1212-12-12	23423423423
95	GGui404	pbkdf2:sha256:50000$96EqWXUJ$65f0091fcf5735090bfaf193d8ac9b02d5a50eb684c846799bbfa4eebb8019b5	Guil2020	GGui777@getsave.io	32112312312	3	2		1	0	no location	2017-10-22 19:41:24.075803	418-806-605	1212-12-12	123123123213
97	MA512	pbkdf2:sha256:50000$NMhyJ0Xn$67740ef83ddc969544b99121beb9af8ee4984e37995ee7440485e2b13941fede	Member A	MA342@getsave.io	12344443	3	2		1	0	no location	2017-10-26 15:06:11.083538	437-20-996	2018-02-11	234423423
99	AASD339	pbkdf2:sha256:50000$NXfYlmsL$f39de15724c9942dafda9ec6185334682e0d7762fa510abeeedbce9ff4bf54d3	ASDAS	AASD138@getsave.io	123423423	3	1		1	0	no location	2017-10-26 15:06:11.083538	437-20-996	2019-12-12	234234234
101	NUmu836	pbkdf2:sha256:50000$KPeVwdg3$d18b3a8fb9611d22bfe88114b25cfcd5e11f9294689c31e4fd9a0f34def715e6	Nicole Umurungi	NUmu026@getsave.io	788881674	3	2		1	0	no location	2017-10-26 15:41:02.229303	932-98-180	1994-10-10	11994555334455
104	NUmu753	pbkdf2:sha256:50000$LhN7bLXO$01ea6e7a27b4a0080fa46f061b7d508535c4ccd3c6e2b36698f4a6819e6dcec8	Nicole Umurungi	NUmu838@getsave.io	250788881674	3	2		1	0	no location	2017-10-26 15:41:02.024158	245-713-235	1994-10-10	119945553378455
105	stanl	pbkdf2:sha256:50000$xvFwD5NA$0d9cee6922b843cbd06c8a762572173be8a987d623e2f186a71fe96ad8a1ed02	Stanley	stanley@exuus.com	250728683008	3	1	Bachelor	1	0	no location	2017-10-26 16:55:06.493393	56-957-55	1991-01-01	123122122456216
2	mjessy	pbkdf2:sha256:50000$g7WQliOa$e355cc4cdae995fd9d07b7c36fd3af481a713efb32e9f225f55854ddd609079e	Jessica Munyana	Munyanajessy@gmail.com	250789265826	2	1	\N	\N	\N	\N	\N	\N	\N	\N
106	philipek	pbkdf2:sha256:50000$svOQwgdL$cb9b8a4016b9c66d69c32c1af6ab9a5e84b91c66154c579c7f88306f4b8916f0	Philip Gakuru	philipek@getsave.io	250722123051	3	1	Bachelor	1	0	kigali	2017-11-07 13:42:42.533807	133-290-841	1991-01-01	1234512066
107	sharif	pbkdf2:sha256:50000$L54XgCiF$c50caf121d4e87a3869ea2b319f91a0865e39bef6a662e816f6749c3d461a3e2	Sharif Tigo	sharift@getsave.io	250722123270	3	1	Bachelor	1	0	kigali	2017-11-07 13:42:42.529735	582-857-828	1991-01-01	123400512066
110	AASD459	pbkdf2:sha256:50000$ovys2rIj$92bdf45d1361c801c5281efd0126431beb4d1be199e78237f72acbd40ce42a9f	ASD	AASD244@getsave.io	77	3	1		1	0	null	2017-11-13 17:48:05.61192	742-848-42	1212-12-12	123111111
111	AADF572	pbkdf2:sha256:50000$CKXRzlO5$f09f77300816285f4259e9febded615e6e79ed87da3b78a61cff7b3bcaed11a7	ADFDF	AADF703@getsave.io	250788776644	3	2		1	0	null	2017-11-13 17:48:05.241122	702-595-68	2017-11-13	998877665545
113	AALE272	pbkdf2:sha256:50000$ZgiCaY7s$e5c79037aa5b998215f94d3479f5e32bdc0fdc0a6ded726c7970ea786387f561	ALEX	AALE173@getsave.io	25078833	3	1		1	1	null	2017-11-13 17:48:06.350793	814-431-653	1212-12-12	23423433333
114	AAle712	pbkdf2:sha256:50000$FAGVQmMf$601e8e53bd8e72a91de5d94ecd646cc3fbb522287fbf43dcb960f165927d6232	Alex	AAle117@getsave.io	2508444777	3	1		1	0	null	2017-11-13 17:48:06.350793	814-431-653	2018-12-12	111144
115	AAli884	pbkdf2:sha256:50000$z3aVcSuI$a298686853b9a83b881242d52d190f7664a6d33dfdfd05671075c76014900b50	Aline	AAli216@getsave.io	250877777	3	1		1	1	null	2017-11-13 17:48:05.241122	702-595-68	2017-12-12	4455667788
116	AALE211	pbkdf2:sha256:50000$gKsRdL14$5f9c6e443ad0f8b58c1570cba3a150cb8047ddb6b5dbaa7436d5188ea5eda054	ALEX	AALE402@getsave.io	250788888	3	1		1	1	null	2017-11-13 17:50:10.19897	167-827-52	1212-12-12	2134324
117	AASD149	pbkdf2:sha256:50000$wgjMxEP4$50fc2070c4171331ce53bd4ed211a154b6d2fbd7329183aec388d76ecf265df2	ASD	AASD351@getsave.io	2334444444	3	1		1	1	null	2017-11-13 17:48:05.241122	702-595-68	1212-12-12	22222
118	GGui217	pbkdf2:sha256:50000$jSmWwr3p$6a147d7a7d6da99cd6538a609f84e2ea011467fb6a6ecda028f02b983fcc33ff	Guil	GGui461@getsave.io	2506873	3	1		1	0	null	2017-11-13 17:48:05.496083	677-949-130	2018-02-12	324234
119	AAle487	pbkdf2:sha256:50000$zOEvlcAy$62d7fc95062073a3ad6ca195d73a99d1275bc7f52759ae822676a7ecb04688b1	Alexxx	AAle834@getsave.io	25075555563	3	1		1	1	null	2017-11-13 17:48:05.496083	677-949-130	2018-12-12	32423423
120	AALE044	pbkdf2:sha256:50000$ajFIJqhe$0585ff17804cb9a87fa0f8caa893464c28c56d41d51d7505df8c94c5f887d99b	ALEX	AALE817@getsave.io	2544444	3	1		1	1	null	2017-11-13 17:48:05.61192	742-848-42	1212-12-12	234234222222
121	YY67891	pbkdf2:sha256:50000$eeGfr0zE$f199385ce3857ff5d17a7cda6f7f33049ea50247f4fec2f1faa0db1dce896cce	Y678	YY67840@getsave.io	2456677	3	1		1	0	null	2017-11-13 17:48:05.241122	702-595-68	2222-02-12	24523
123	MA460	pbkdf2:sha256:50000$GUoKy8Fi$e19814c0b665442276b566ffe9867302d5a1acc3cfe4fc8d19df8aa1271689c7	Member A	MA653@getsave.io	4444444	3	1		1	0	null	2017-11-13 17:50:10.19897	167-827-52	1212-02-11	5666666
124	KKen725	pbkdf2:sha256:50000$cC2jqUVn$8783a8a02b140f1a3aa21fba6b592d9a4de01ec860592c15bebd86697ded2e9d	Kenessa	KKen130@getsave.io	24566666	3	2		1	1	null	2017-11-13 21:08:06.557511	832-393-460	1212-12-12	12222222
126	AGro430	pbkdf2:sha256:50000$5mTDXBlj$0f6dce9c25886ba0f48f4b444bb0a14939e5714e7701bd7a329defd74d3c3353	ABC Group	AGro886@getsave.io	25078888883	3	2		1	1	null	2017-11-13 21:08:12.202135	326-626-270	1200-12-12	23423423555555
128	MA450	pbkdf2:sha256:50000$EvGXVlxf$80dad66b82ee8e040826c8be1766a0b58f0745cfef70295acfd098fb4dd08342	Member A	MA820@getsave.io	25078866666	3	1		1	1	null	2017-11-13 21:08:06.958348	718-868-981	2019-12-12	2342444444
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('users_id_seq', 128, true);


--
-- Data for Name: village; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY village (id, name, code) FROM stdin;
1	imanzi	\N
2	imanzi	\N
3	kibaza	003458
\.


--
-- Name: village_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('village_id_seq', 4, true);


--
-- Name: alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: intervention_area_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY intervention_area
    ADD CONSTRAINT intervention_area_pkey PRIMARY KEY (id);


--
-- Name: meeting_attendance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY meeting_attendance
    ADD CONSTRAINT meeting_attendance_pkey PRIMARY KEY (id);


--
-- Name: member_approved_loan_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_approved_loan
    ADD CONSTRAINT member_approved_loan_pkey PRIMARY KEY (id);


--
-- Name: member_approved_social_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_approved_social
    ADD CONSTRAINT member_approved_social_pkey PRIMARY KEY (id);


--
-- Name: member_fine_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_fine
    ADD CONSTRAINT member_fine_pkey PRIMARY KEY (id);


--
-- Name: member_loan_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_loan
    ADD CONSTRAINT member_loan_pkey PRIMARY KEY (id);


--
-- Name: member_social_fund_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_social_fund
    ADD CONSTRAINT member_social_fund_pkey PRIMARY KEY (id);


--
-- Name: members_mini_statement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY members_mini_statement
    ADD CONSTRAINT members_mini_statement_pkey PRIMARY KEY (id);


--
-- Name: organization_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY organization
    ADD CONSTRAINT organization_email_key UNIQUE (email);


--
-- Name: organization_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY organization
    ADD CONSTRAINT organization_pkey PRIMARY KEY (id);


--
-- Name: project_agent_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY project_agent
    ADD CONSTRAINT project_agent_pkey PRIMARY KEY (id);


--
-- Name: project_partner_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY project_partner
    ADD CONSTRAINT project_partner_pkey PRIMARY KEY (id);


--
-- Name: project_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY project
    ADD CONSTRAINT project_pkey PRIMARY KEY (id);


--
-- Name: saving_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY saving_group
    ADD CONSTRAINT saving_group_name_key UNIQUE (name);


--
-- Name: saving_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY saving_group
    ADD CONSTRAINT saving_group_pkey PRIMARY KEY (id);


--
-- Name: saving_group_shares_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY saving_group_shares
    ADD CONSTRAINT saving_group_shares_pkey PRIMARY KEY (id);


--
-- Name: sg_cycle_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_cycle
    ADD CONSTRAINT sg_cycle_pkey PRIMARY KEY (id);


--
-- Name: sg_drop_out_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_drop_out
    ADD CONSTRAINT sg_drop_out_pkey PRIMARY KEY (id);


--
-- Name: sg_fin_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_fin_details
    ADD CONSTRAINT sg_fin_details_pkey PRIMARY KEY (id);


--
-- Name: sg_fines_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_fines
    ADD CONSTRAINT sg_fines_pkey PRIMARY KEY (id);


--
-- Name: sg_meeting_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_meeting
    ADD CONSTRAINT sg_meeting_pkey PRIMARY KEY (id);


--
-- Name: sg_member_contributions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_member_contributions
    ADD CONSTRAINT sg_member_contributions_pkey PRIMARY KEY (id);


--
-- Name: sg_member_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_member
    ADD CONSTRAINT sg_member_pkey PRIMARY KEY (id);


--
-- Name: sg_wallet_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_wallet
    ADD CONSTRAINT sg_wallet_pkey PRIMARY KEY (id);


--
-- Name: user_fin_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_fin_details
    ADD CONSTRAINT user_fin_details_pkey PRIMARY KEY (id);


--
-- Name: users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users_id_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_id_number_key UNIQUE (id_number);


--
-- Name: users_phone_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_phone_key UNIQUE (phone);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: village_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY village
    ADD CONSTRAINT village_code_key UNIQUE (code);


--
-- Name: village_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY village
    ADD CONSTRAINT village_pkey PRIMARY KEY (id);


--
-- Name: ix_intervention_area_project_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_intervention_area_project_id ON intervention_area USING btree (project_id);


--
-- Name: ix_intervention_area_village_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_intervention_area_village_id ON intervention_area USING btree (village_id);


--
-- Name: ix_meeting_attendance_member_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_meeting_attendance_member_id ON meeting_attendance USING btree (member_id);


--
-- Name: ix_meeting_attendance_sg_meeting_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_meeting_attendance_sg_meeting_id ON meeting_attendance USING btree (sg_meeting_id);


--
-- Name: ix_member_approved_loan_loan_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_member_approved_loan_loan_id ON member_approved_loan USING btree (loan_id);


--
-- Name: ix_member_approved_loan_sg_member_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_member_approved_loan_sg_member_id ON member_approved_loan USING btree (sg_member_id);


--
-- Name: ix_member_approved_social_sg_member_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_member_approved_social_sg_member_id ON member_approved_social USING btree (sg_member_id);


--
-- Name: ix_member_approved_social_social_debit_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_member_approved_social_social_debit_id ON member_approved_social USING btree (social_debit_id);


--
-- Name: ix_member_fine_cycle_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_member_fine_cycle_id ON member_fine USING btree (cycle_id);


--
-- Name: ix_member_fine_member_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_member_fine_member_id ON member_fine USING btree (member_id);


--
-- Name: ix_member_fine_wallet_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_member_fine_wallet_id ON member_fine USING btree (wallet_id);


--
-- Name: ix_member_loan_sg_cycle_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_member_loan_sg_cycle_id ON member_loan USING btree (sg_cycle_id);


--
-- Name: ix_member_loan_sg_member_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_member_loan_sg_member_id ON member_loan USING btree (sg_member_id);


--
-- Name: ix_member_loan_sg_wallet_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_member_loan_sg_wallet_id ON member_loan USING btree (sg_wallet_id);


--
-- Name: ix_member_social_fund_sg_cycle_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_member_social_fund_sg_cycle_id ON member_social_fund USING btree (sg_cycle_id);


--
-- Name: ix_member_social_fund_sg_member_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_member_social_fund_sg_member_id ON member_social_fund USING btree (sg_member_id);


--
-- Name: ix_member_social_fund_sg_wallet_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_member_social_fund_sg_wallet_id ON member_social_fund USING btree (sg_wallet_id);


--
-- Name: ix_members_mini_statement_member_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_members_mini_statement_member_id ON members_mini_statement USING btree (member_id);


--
-- Name: ix_organization_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_organization_name ON organization USING btree (name);


--
-- Name: ix_project_agent_project_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_project_agent_project_id ON project_agent USING btree (project_id);


--
-- Name: ix_project_agent_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_project_agent_user_id ON project_agent USING btree (user_id);


--
-- Name: ix_project_organization_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_project_organization_id ON project USING btree (organization_id);


--
-- Name: ix_project_partner_project_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_project_partner_project_id ON project_partner USING btree (project_id);


--
-- Name: ix_project_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_project_user_id ON project USING btree (user_id);


--
-- Name: ix_saving_group_agent_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_saving_group_agent_id ON saving_group USING btree (agent_id);


--
-- Name: ix_saving_group_organization_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_saving_group_organization_id ON saving_group USING btree (organization_id);


--
-- Name: ix_saving_group_project_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_saving_group_project_id ON saving_group USING btree (project_id);


--
-- Name: ix_saving_group_shares_saving_group_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_saving_group_shares_saving_group_id ON saving_group_shares USING btree (saving_group_id);


--
-- Name: ix_saving_group_shares_sg_cycle_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_saving_group_shares_sg_cycle_id ON saving_group_shares USING btree (sg_cycle_id);


--
-- Name: ix_saving_group_village_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_saving_group_village_id ON saving_group USING btree (village_id);


--
-- Name: ix_sg_cycle_saving_group_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sg_cycle_saving_group_id ON sg_cycle USING btree (saving_group_id);


--
-- Name: ix_sg_drop_out_sg_cycle_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sg_drop_out_sg_cycle_id ON sg_drop_out USING btree (sg_cycle_id);


--
-- Name: ix_sg_drop_out_sg_member_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sg_drop_out_sg_member_id ON sg_drop_out USING btree (sg_member_id);


--
-- Name: ix_sg_fin_details_saving_group_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sg_fin_details_saving_group_id ON sg_fin_details USING btree (saving_group_id);


--
-- Name: ix_sg_fines_saving_group_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sg_fines_saving_group_id ON sg_fines USING btree (saving_group_id);


--
-- Name: ix_sg_fines_sg_cycle_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sg_fines_sg_cycle_id ON sg_fines USING btree (sg_cycle_id);


--
-- Name: ix_sg_meeting_cycle_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sg_meeting_cycle_id ON sg_meeting USING btree (cycle_id);


--
-- Name: ix_sg_meeting_saving_group_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sg_meeting_saving_group_id ON sg_meeting USING btree (saving_group_id);


--
-- Name: ix_sg_member_contributions_sg_cycle_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sg_member_contributions_sg_cycle_id ON sg_member_contributions USING btree (sg_cycle_id);


--
-- Name: ix_sg_member_contributions_sg_member_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sg_member_contributions_sg_member_id ON sg_member_contributions USING btree (sg_member_id);


--
-- Name: ix_sg_member_contributions_sg_wallet_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sg_member_contributions_sg_wallet_id ON sg_member_contributions USING btree (sg_wallet_id);


--
-- Name: ix_sg_member_pin; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sg_member_pin ON sg_member USING btree (pin);


--
-- Name: ix_sg_member_saving_group_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sg_member_saving_group_id ON sg_member USING btree (saving_group_id);


--
-- Name: ix_sg_member_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sg_member_user_id ON sg_member USING btree (user_id);


--
-- Name: ix_sg_wallet_saving_group_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_sg_wallet_saving_group_id ON sg_wallet USING btree (saving_group_id);


--
-- Name: ix_user_fin_details_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_fin_details_user_id ON user_fin_details USING btree (user_id);


--
-- Name: ix_users_organization_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_organization_id ON users USING btree (organization_id);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_username ON users USING btree (username);


--
-- Name: member_sg_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX member_sg_index ON sg_member USING btree (saving_group_id, user_id);


--
-- Name: unique_attendee; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX unique_attendee ON meeting_attendance USING btree (sg_meeting_id, member_id);


--
-- Name: unique_cycle; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX unique_cycle ON sg_cycle USING btree (start, "end", saving_group_id);


--
-- Name: unique_fine; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX unique_fine ON sg_fines USING btree (saving_group_id, sg_cycle_id);


--
-- Name: unique_share; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX unique_share ON saving_group_shares USING btree (saving_group_id, sg_cycle_id);


--
-- Name: intervention_area_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY intervention_area
    ADD CONSTRAINT intervention_area_project_id_fkey FOREIGN KEY (project_id) REFERENCES project(id);


--
-- Name: intervention_area_village_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY intervention_area
    ADD CONSTRAINT intervention_area_village_id_fkey FOREIGN KEY (village_id) REFERENCES village(id);


--
-- Name: meeting_attendance_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY meeting_attendance
    ADD CONSTRAINT meeting_attendance_member_id_fkey FOREIGN KEY (member_id) REFERENCES sg_member(id);


--
-- Name: meeting_attendance_sg_meeting_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY meeting_attendance
    ADD CONSTRAINT meeting_attendance_sg_meeting_id_fkey FOREIGN KEY (sg_meeting_id) REFERENCES sg_meeting(id);


--
-- Name: member_approved_loan_loan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_approved_loan
    ADD CONSTRAINT member_approved_loan_loan_id_fkey FOREIGN KEY (loan_id) REFERENCES member_loan(id);


--
-- Name: member_approved_loan_sg_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_approved_loan
    ADD CONSTRAINT member_approved_loan_sg_member_id_fkey FOREIGN KEY (sg_member_id) REFERENCES sg_member(id);


--
-- Name: member_approved_social_sg_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_approved_social
    ADD CONSTRAINT member_approved_social_sg_member_id_fkey FOREIGN KEY (sg_member_id) REFERENCES sg_member(id);


--
-- Name: member_approved_social_social_debit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_approved_social
    ADD CONSTRAINT member_approved_social_social_debit_id_fkey FOREIGN KEY (social_debit_id) REFERENCES member_social_fund(id);


--
-- Name: member_fine_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_fine
    ADD CONSTRAINT member_fine_cycle_id_fkey FOREIGN KEY (cycle_id) REFERENCES sg_cycle(id);


--
-- Name: member_fine_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_fine
    ADD CONSTRAINT member_fine_member_id_fkey FOREIGN KEY (member_id) REFERENCES sg_member(id);


--
-- Name: member_fine_wallet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_fine
    ADD CONSTRAINT member_fine_wallet_id_fkey FOREIGN KEY (wallet_id) REFERENCES sg_wallet(id);


--
-- Name: member_loan_sg_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_loan
    ADD CONSTRAINT member_loan_sg_cycle_id_fkey FOREIGN KEY (sg_cycle_id) REFERENCES sg_cycle(id);


--
-- Name: member_loan_sg_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_loan
    ADD CONSTRAINT member_loan_sg_member_id_fkey FOREIGN KEY (sg_member_id) REFERENCES sg_member(id);


--
-- Name: member_loan_sg_wallet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_loan
    ADD CONSTRAINT member_loan_sg_wallet_id_fkey FOREIGN KEY (sg_wallet_id) REFERENCES sg_wallet(id);


--
-- Name: member_social_fund_sg_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_social_fund
    ADD CONSTRAINT member_social_fund_sg_cycle_id_fkey FOREIGN KEY (sg_cycle_id) REFERENCES sg_cycle(id);


--
-- Name: member_social_fund_sg_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_social_fund
    ADD CONSTRAINT member_social_fund_sg_member_id_fkey FOREIGN KEY (sg_member_id) REFERENCES sg_member(id);


--
-- Name: member_social_fund_sg_wallet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY member_social_fund
    ADD CONSTRAINT member_social_fund_sg_wallet_id_fkey FOREIGN KEY (sg_wallet_id) REFERENCES sg_wallet(id);


--
-- Name: members_mini_statement_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY members_mini_statement
    ADD CONSTRAINT members_mini_statement_member_id_fkey FOREIGN KEY (member_id) REFERENCES sg_member(id);


--
-- Name: project_agent_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY project_agent
    ADD CONSTRAINT project_agent_project_id_fkey FOREIGN KEY (project_id) REFERENCES project(id);


--
-- Name: project_agent_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY project_agent
    ADD CONSTRAINT project_agent_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: project_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY project
    ADD CONSTRAINT project_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES organization(id);


--
-- Name: project_partner_partner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY project_partner
    ADD CONSTRAINT project_partner_partner_id_fkey FOREIGN KEY (partner_id) REFERENCES organization(id);


--
-- Name: project_partner_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY project_partner
    ADD CONSTRAINT project_partner_project_id_fkey FOREIGN KEY (project_id) REFERENCES project(id);


--
-- Name: project_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY project
    ADD CONSTRAINT project_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: saving_group_agent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY saving_group
    ADD CONSTRAINT saving_group_agent_id_fkey FOREIGN KEY (agent_id) REFERENCES users(id);


--
-- Name: saving_group_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY saving_group
    ADD CONSTRAINT saving_group_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES organization(id);


--
-- Name: saving_group_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY saving_group
    ADD CONSTRAINT saving_group_project_id_fkey FOREIGN KEY (project_id) REFERENCES project(id);


--
-- Name: saving_group_shares_saving_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY saving_group_shares
    ADD CONSTRAINT saving_group_shares_saving_group_id_fkey FOREIGN KEY (saving_group_id) REFERENCES saving_group(id);


--
-- Name: saving_group_shares_sg_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY saving_group_shares
    ADD CONSTRAINT saving_group_shares_sg_cycle_id_fkey FOREIGN KEY (sg_cycle_id) REFERENCES sg_cycle(id);


--
-- Name: saving_group_village_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY saving_group
    ADD CONSTRAINT saving_group_village_id_fkey FOREIGN KEY (village_id) REFERENCES village(id);


--
-- Name: sg_cycle_saving_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_cycle
    ADD CONSTRAINT sg_cycle_saving_group_id_fkey FOREIGN KEY (saving_group_id) REFERENCES saving_group(id);


--
-- Name: sg_drop_out_sg_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_drop_out
    ADD CONSTRAINT sg_drop_out_sg_cycle_id_fkey FOREIGN KEY (sg_cycle_id) REFERENCES sg_cycle(id);


--
-- Name: sg_drop_out_sg_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_drop_out
    ADD CONSTRAINT sg_drop_out_sg_member_id_fkey FOREIGN KEY (sg_member_id) REFERENCES sg_member(id);


--
-- Name: sg_fin_details_saving_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_fin_details
    ADD CONSTRAINT sg_fin_details_saving_group_id_fkey FOREIGN KEY (saving_group_id) REFERENCES saving_group(id);


--
-- Name: sg_fines_saving_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_fines
    ADD CONSTRAINT sg_fines_saving_group_id_fkey FOREIGN KEY (saving_group_id) REFERENCES saving_group(id);


--
-- Name: sg_fines_sg_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_fines
    ADD CONSTRAINT sg_fines_sg_cycle_id_fkey FOREIGN KEY (sg_cycle_id) REFERENCES sg_cycle(id);


--
-- Name: sg_meeting_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_meeting
    ADD CONSTRAINT sg_meeting_cycle_id_fkey FOREIGN KEY (cycle_id) REFERENCES sg_cycle(id);


--
-- Name: sg_meeting_saving_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_meeting
    ADD CONSTRAINT sg_meeting_saving_group_id_fkey FOREIGN KEY (saving_group_id) REFERENCES saving_group(id);


--
-- Name: sg_member_contributions_sg_cycle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_member_contributions
    ADD CONSTRAINT sg_member_contributions_sg_cycle_id_fkey FOREIGN KEY (sg_cycle_id) REFERENCES sg_cycle(id);


--
-- Name: sg_member_contributions_sg_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_member_contributions
    ADD CONSTRAINT sg_member_contributions_sg_member_id_fkey FOREIGN KEY (sg_member_id) REFERENCES sg_member(id);


--
-- Name: sg_member_contributions_sg_wallet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_member_contributions
    ADD CONSTRAINT sg_member_contributions_sg_wallet_id_fkey FOREIGN KEY (sg_wallet_id) REFERENCES sg_wallet(id);


--
-- Name: sg_member_saving_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_member
    ADD CONSTRAINT sg_member_saving_group_id_fkey FOREIGN KEY (saving_group_id) REFERENCES saving_group(id);


--
-- Name: sg_member_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_member
    ADD CONSTRAINT sg_member_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: sg_wallet_saving_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sg_wallet
    ADD CONSTRAINT sg_wallet_saving_group_id_fkey FOREIGN KEY (saving_group_id) REFERENCES saving_group(id);


--
-- Name: user_fin_details_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_fin_details
    ADD CONSTRAINT user_fin_details_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: users_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES organization(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

