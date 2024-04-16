import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from models.accidents import *
from models.aggregates import *
from models.brandsteel import *
from models.cranes import *
from models.dynamics import *
from models.employees import *
from models.jwt import *
from models.ladles import *
from models.routes import *
from config import settings
from database import Base, engine, session_factory


class DBModeException(BaseException):
    """
    Исключение режима БД.
    Если MODE = DEV, то будет вызвана эта ошбика
    """
    default_code: str = 'Invalid database mode'
    default_detail: str = 'Tests wont work if database mode is DEV, mode must be TEST'

    def __init__(self, code=None, detail=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = f'Code: {code}. Detail: {detail}'

    def __str__(self):
        return str(self.detail)


@pytest_asyncio.fixture(scope='package', autouse=False)
async def session() -> AsyncSession:
    """Инициализация БД"""
    # Проверка режима БД. Тут нужно убедиться, что изменения будут происходить
    # с тестовой БД.
    if settings.MODE != 'TEST':
        raise DBModeException
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(
            text(
                '''
                INSERT INTO public.visual_aggregates (id, title, num_agg, num_pos, coord_x, coord_y, stay_time, photo, is_broken) VALUES
                    (7, 'ГМП', '1', '1', 985, 271, '00:50:00', 'photos/aggregates/kovsh_w_m.png', false),
                    (8, 'ГМП', '2', '1', 707, 271, '00:50:00', 'photos/aggregates/kovsh_w_m_hH9WEq5.png', false),
                    (9, 'УКП', '1', '1', 81, 331, '00:40:00', 'photos/aggregates/full_kovsh.png', false),
                    (10, 'УКП', '1', '2', 162, 321, '00:40:00', 'photos/aggregates/full_kovsh_xAD2IT7.png', false),
                    (11, 'УКП', '2', '1', 1100, 221, '00:40:00', 'photos/aggregates/full_kovsh_TjRi4Cl.png', false),
                    (12, 'УКП', '2', '2', 1183, 211, '00:40:00', 'photos/aggregates/full_kovsh_yyNgzoh.png', false),
                    (13, 'УВС', '1', '1', 974, 421, '00:50:00', 'photos/aggregates/kovsh_w_m_3yqBgPt.png', false),
                    (14, 'УВС', '1', '2', 894, 431, '00:50:00', 'photos/aggregates/kovsh_w_m_pFo8IJd.png', false),
                    (15, 'МНЛЗ', '1', '1', 660, 441, '01:10:00', 'photos/aggregates/kovsh_w_m_W6zlGOU.png', false),
                    (16, 'МНЛЗ', '2', '1', 416, 441, '00:50:00', 'photos/aggregates/kovsh_w_m_WmddaeI.png', false),
                    (22, 'Горелка', '1', '1', 475, 261, '00:20:00', 'photos/aggregates/kovsh_w_m_PX6d53Q.png', false),
                    (23, 'Горелка', '1', '2', 530, 261, '00:20:00', 'photos/aggregates/kovsh_w_m_Ja2RNyL.png', false),
                    (24, 'Горелка', '1', '3', 590, 261, '00:20:00', 'photos/aggregates/kovsh_w_m_AKFORuC.png', false),
                    (25, 'Лежка', '1', '1', 770, 240, '00:20:00', 'photos/aggregates/h_kovsh_GZGLs09.png', false),
                    (26, 'Лежка', '1', '2', 645, 220, '00:20:00', 'photos/aggregates/h_kovsh_fUKMWkJ.png', false);
                '''
            )
        )
        await conn.execute(
            text(
                '''
                INSERT INTO public.visual_aggregatesburner (aggregates_ptr_id) VALUES
                    (22),
                    (23),
                    (24);
                '''
            )
        )
        await conn.execute(
            text(
                '''
                INSERT INTO public.visual_aggregatesgmp (aggregates_ptr_id) VALUES
                    (7),
                    (8);
                '''
            )
        )
        await conn.execute(
            text(
                '''
                INSERT INTO public.visual_aggregatesl (aggregates_ptr_id) VALUES
                    (25),
                    (26);
                '''
            )
        )
        await conn.execute(
            text(
                '''
                INSERT INTO public.visual_aggregatesmnlz (aggregates_ptr_id) VALUES
                    (15),
                    (16);
                '''
            )
        )
        await conn.execute(
            text(
                '''
                INSERT INTO public.visual_aggregatesukp (aggregates_ptr_id) VALUES
                    (9),
                    (10),
                    (11),
                    (12);
                '''
            )
        )
        await conn.execute(
            text(
                '''
                INSERT INTO public.visual_aggregatesuvs (aggregates_ptr_id) VALUES
                    (13),
                    (14);
                '''
            )
        )
        await conn.execute(
            text(
                '''
                INSERT INTO public.visual_brandsteel (id, title) VALUES
                    (1, '10ХСНД'),
                    (2, 'СТ2'),
                    (3, '09Г2С'),
                    (4, 'СТТ');
                '''
            )
        )
        await conn.execute(
            text(
                '''
                INSERT INTO public.visual_cranes (id, title, size_x, size_y, photo, is_broken) VALUES
                    (1, 'Кран 7', 22, 338, 'korpus.png', false),
                    (2, 'Кран 8', 22, 338, 'korpus_JJLfH8t.png', false),
                    (3, 'Кран 9', 22, 338, 'korpus_gFeLkxy.png', false),
                    (4, 'Кран 10', 22, 338, 'korpus_VcLTltX.png', false),
                    (5, 'Каретка_д_в', 35, 35, 'caretka_d_w.png', false),
                    (6, 'Каретка_д_во', 35, 35, 'caretka_d_wo.png', false),
                    (7, 'Каретка_у_в', 35, 35, 'caretka_u_w.png', false),
                    (8, 'Каретка_у_во', 35, 35, 'caretka_u_wo.png', false);
                '''
            )
        )
        await conn.execute(
            text(
                '''
                INSERT INTO public.visual_employees (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, send_messages, photo, post, patronymic, slug) VALUES (1, 'pbkdf2_sha256$600000$f9itIUq6nRy9K5vKAg8vWY$2qsEnuKrBOINZng4yrqKCHPbKBOrYjv3r852vhvMu5k=', '2023-11-29 20:59:59.950288+05', true, 'root', 'Vladyslav', 'Kravchenko', 'root@gmail.com', true, true, '2023-11-25 20:16:44.720751+05', true, 'photos/kravasos/авановая.jpg', 'MS', 'Alexandrovich', 'root');
                '''
            )
        )
        await conn.execute(
            text(
                '''
                INSERT INTO public.visual_ladles (title, is_active, is_broken) VALUES
                    ('Ковш 1', false, false),
                    ('Ковш 2', false, false),
                    ('Ковш 3', false, false),
                    ('Ковш 4', false, false),
                    ('Ковш 5', false, false),
                    ('Ковш 6', false, false),
                    ('Ковш 7', false, false),
                    ('Ковш 8', false, false),
                    ('Ковш 9', false, false),
                    ('Ковш 10', false, false);
                '''
            )
        )
        await conn.execute(
            text(
                '''
                INSERT INTO public.visual_routes (id, aggregate_1_id, aggregate_2_id, aggregate_3_id, aggregate_4_id) VALUES
                    (1, 8, 9, 14, 16),
                    (2, 8, 10, 14, 16),
                    (3, 7, 11, 13, 15),
                    (4, 7, 12, 13, 15);
                '''
            )
        )
        await conn.execute(
            text(
                '''
                INSERT INTO public.visual_activedynamictable (id, num_melt, brand_steel_id, plan_start, plan_end, actual_start, actual_end, aggregate_id, ladle_id, route_id) VALUES
                    (1, 'Z32100', 1, '2023-12-11 12:00:00+05', '2023-12-11 12:50:00+05', '2023-12-11 12:00:00+05', '2023-12-11 12:50:00+05', 8, 1, 1),
                    (2, 'Z32100', 1, '2023-12-11 12:55:00+05', '2023-12-11 13:35:00+05', '2023-12-11 12:55:00+05', '2023-12-11 13:35:00+05', 9, 1, 1),
                    (3, 'Z32100', 1, '2023-12-11 13:40:00+05', '2023-12-11 14:30:00+05', '2023-12-11 13:40:00+05', '2023-12-11 14:30:00+05', 14, 1, 1),
                    (4, 'Z32100', 1, '2023-12-11 14:35:00+05', '2023-12-11 15:25:00+05', '2023-12-11 14:35:00+05', '2023-12-11 15:25:00+05', 16, 1, 1),
                    (5, 'V32100', 2, '2023-12-11 12:30:00+05', '2023-12-11 13:20:00+05', '2023-12-11 12:30:00+05', '2023-12-11 13:20:00+05', 7, 2, 3),
                    (6, 'V32100', 2, '2023-12-11 13:25:00+05', '2023-12-11 14:05:00+05', '2023-12-11 13:25:00+05', '2023-12-11 14:05:00+05', 11, 2, 3),
                    (7, 'V32100', 2, '2023-12-11 14:10:00+05', '2023-12-11 15:00:00+05', '2023-12-11 14:10:00+05', '2023-12-11 15:00:00+05', 13, 2, 3),
                    (8, 'V32100', 2, '2023-12-11 15:05:00+05', '2023-12-11 16:15:00+05', '2023-12-11 15:05:00+05', '2023-12-11 16:15:00+05', 15, 2, 3),
                    (9, 'Z32101', 1, '2023-12-11 13:00:00+05', '2023-12-11 13:50:00+05', '2023-12-11 13:00:00+05', '2023-12-11 13:50:00+05', 8, 3, 2),
                    (10, 'Z32101', 1, '2023-12-11 13:55:00+05', '2023-12-11 14:35:00+05', '2023-12-11 13:55:00+05', '2023-12-11 14:35:00+05', 10, 3, 2),
                    (11, 'Z32101', 1, '2023-12-11 14:40:00+05', '2023-12-11 15:30:00+05', '2023-12-11 14:40:00+05', '2023-12-11 15:30:00+05', 14, 3, 2),
                    (12, 'Z32101', 1, '2023-12-11 15:35:00+05', '2023-12-11 16:25:00+05', '2023-12-11 15:35:00+05', '2023-12-11 16:25:00+05', 16, 3, 2);
                '''
            )
        )
        async with session_factory(bind=conn) as session:
            yield session
            await session.commit()
            await session.rollback()


@pytest_asyncio.fixture
def get_auth_user():
    """Получить авторизованного пользователя, токены"""
    ...
