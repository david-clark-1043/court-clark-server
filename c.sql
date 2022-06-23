UPDATE courtzapi_filertype
SET filer_type = "attorney"
WHERE id = 4;
UPDATE courtzapi_filer
SET id = 2
WHERE id = 1;

DELETE FROM courtzapi_filer
WHERE id = 1;

DELETE FROM courtzapi_repfirmparty
WHERE rep_firm_id = 25;
DELETE FROM courtzapi_docketparty
WHERE rep_firm_party_id = 2;

DELETE FROM auth_user
WHERE id = 1;

UPDATE auth_user
SET is_staff = True
WHERE id = 3;

INSERT INTO courtzapi_filertype
VALUES (1, "clerk");
INSERT INTO courtzapi_filertype
VALUES (null, "judge");
INSERT INTO courtzapi_filertype
VALUES (null, "pro se");
INSERT INTO courtzapi_filertype
VALUES (null, "filer");

INSERT INTO courtzapi_casestatus
VALUES (null, "open");
INSERT INTO courtzapi_casestatus
VALUES (null, "closed");

INSERT INTO courtzapi_filingtype
VALUES (null, "complaint");
INSERT INTO courtzapi_filingtype
VALUES (null, "reply");
INSERT INTO courtzapi_filingtype
VALUES (null, "motion");
INSERT INTO courtzapi_filingtype
VALUES (null, "order");

INSERT INTO courtzapi_partytype
VALUES (null, "clerk");
INSERT INTO courtzapi_partytype
VALUES (null, "judge");
INSERT INTO courtzapi_partytype
VALUES (null, "plaintiff");
INSERT INTO courtzapi_partytype
VALUES (null, "defendant");

INSERT INTO courtzapi_firm
VALUES (null, "Dewey, Cheatam, & Howe");
INSERT INTO courtzapi_firm
VALUES (null, "Hamlin, Hamlin, McGill");
INSERT INTO courtzapi_firm
VALUES (null, "pro se");
INSERT INTO courtzapi_firm
VALUES (null, "judge");
INSERT INTO courtzapi_firm
VALUES (null, "clerk");
